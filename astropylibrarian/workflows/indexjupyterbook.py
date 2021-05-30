# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Workflow for ingesting a Jupyter Book site (as a Learn Astropy Guide).

This workflow ingests the Jupyter Book homepage and triggers workflows to
ingest individual Jupyter Book content pages.
"""

from __future__ import annotations

__all__ = ["index_jupyterbook"]

import re
from typing import TYPE_CHECKING, List, Optional, Union
from urllib.parse import urljoin, urlparse, urlunparse

from pydantic import BaseModel, HttpUrl, validator

from astropylibrarian.workflows.download import download_html

if TYPE_CHECKING:
    import aiohttp
    import lxml.html
    from algoliasearch.search_client import SearchClient

    from astropylibrarian.resources import HtmlPage


async def index_jupyterbook(
    *,
    url: str,
    http_client: "aiohttp.ClientSession",
    algolia_client: "SearchClient",
    index_name: str,
) -> List[str]:
    """Ingest a Jupyter Book site as a Learn Astropy Guide.

    Parameters
    ----------
    url : `str`
        A URL for an HTML page.
    http_client : `aiohttp.ClientSession`
        An open aiohttp client.
    algolia_client : `algoliasearch.search_client.SearchClient`
        The Algolia client.
    index_name : `str`
        The full name of the Algolia index to save the records to.

    Returns
    -------
    object_ids : `list` of `str`
        List of Algolia record object IDs that are saved by this indexing
        operation.
    """
    homepage = await download_homepage(url=url, http_client=http_client)
    homepage_metadata = extract_homepage_metadata(
        html_page=homepage, root_url=url
    )
    print(homepage_metadata)
    # TODO create async jobs to download each page
    return []


async def download_homepage(
    *, url: str, http_client: "aiohttp.ClientSession"
) -> HtmlPage:
    """Download the HTML for the Jupyter Book's homepage, given the root
    URL

    This function solves the fact that the root URL hosts a redirect
    page

    Parameters
    ----------
    url : `str`
        The root URL of the Jupyter Book
    http_client : `aiohttp.ClientSession`
        An open aiohttp client.

    Returns
    -------
    astropylibrarian.resources.HtmlPage
        The HTML page.
    """
    index_page = await download_html(url=url, http_client=http_client)

    try:
        # Detect if the URL is a redirect to the true first content page
        redirect_url = detect_redirect(index_page)
        if isinstance(redirect_url, str):
            return await download_html(
                url=redirect_url, http_client=http_client
            )
    except Exception:
        pass

    return index_page


def detect_redirect(html_page: HtmlPage) -> Union[None, str]:
    """Detect if the page is actually an immediate redirect to another page
    via an "http-equiv=Refresh" meta tag.

    Parameters
    ----------
    html_page : `astropylibrarian.resources.HtmlPage`
        The HTML page.

    Returns
    -------
    `None` or `str`
        Returns `None` if the page is not a redirect. If the page *is* a,
        redirect, returns the URL of the target page.
    """
    doc = html_page.parse()
    # Now try to see if there is a <meta> tag with http-equiv="Refresh"
    for element in doc.cssselect("meta"):
        try:
            if element.attrib["http-equiv"].lower() == "refresh":
                return parse_redirect_url(
                    content=element.attrib["content"], source_url=html_page.url
                )
        except (KeyError, RuntimeError):
            continue

    return None


def parse_redirect_url(*, content: str, source_url: str) -> str:
    """Parse the http-equiv tag to create the redirect destination URL.

    Parameters
    ----------
    content : `str`
        The ``content`` attribute of the meta tag.
    source_url : `str`
        The URL of the page hosting the meta tag.

    Returns
    -------
    str
        The target URL of the redirection.

    Raises
    ------
    RuntimeError
        Raised if the content cannot be parsed.

    Examples
    --------
    >>> content = "0; url=notebooks/00-00-Preface.html"
    >>> source_url = "https://example.org/index.html"
    >>> parse_redirect_url(content=content, source_url=source_url)
    'https://example.org/notebooks/00-00-Preface.html'
    """
    m = re.match(r"\d+; url=(.+)", content)
    if m:
        redirect_path = m.group(1)
    else:
        raise RuntimeError("No url match")

    return urljoin(source_url, redirect_path)


def extract_homepage_metadata(
    *, html_page: HtmlPage, root_url: str
) -> JupyterBookMetadata:
    """Extract JupyterBook project metadata from it's homepage.

    Parameters
    ----------
    html_page : astropylibrarian.resources.HtmlPage
        The downloaded JupyterBook homepage, see `download_homepage`.
    root_url : str
        The root URL of the JupyterBook. This value is typically the URL
        input to `index_jupyterbook` and becomes a unique identifier for all
        Algolia records related to a JupyterBook, across all of a JupyterBook's
        pages.

    Returns
    -------
    JupyterBookMetadata
        Metadata associated with the JupyterBook project.
    """
    homepage = JupyterBookHomepage(html_page)
    md = JupyterBookMetadata(
        root_url=root_url,
        title=homepage.title,
        logo_url=homepage.logo_url,
        description=homepage.first_paragraph or "",
        source_repository=homepage.github_repository,
        page_urls=homepage.page_urls,
    )
    return md


class JupyterBookHomepage:
    """A JupyterBook homepage HTML, with accessors to key content."""

    def __init__(self, html_page: HtmlPage):
        self.html_page = html_page
        self._doc = self.html_page.parse()

    @property
    def doc(self) -> lxml.html.HtmlElement:
        return self._doc

    @property
    def title(self) -> Optional[str]:
        """The site's title (selector: ``#site-title``)."""
        try:
            element = self.doc.cssselect("#site-title")[0]
        except IndexError:
            return None
        return element.text_content()

    @property
    def logo_url(self) -> Optional[str]:
        """The URL of the site's logo (selector: ``img.logo``)."""
        try:
            element = self.doc.cssselect("img.logo")[0]
        except IndexError:
            return None
        return urljoin(self.html_page.url, element.attrib["src"])

    @property
    def first_paragraph(self) -> Optional[str]:
        """The content of the first paragraph within the main content
        (``#main-content``).
        """
        try:
            first_paragraph = self.doc.cssselect("#main-content p")[0]
        except IndexError:
            return None
        content = first_paragraph.text_content()
        return self._clean_content(content)

    @property
    def github_repository(self) -> Optional[str]:
        """The GitHub repository URL, detected in the ``<nav>`` element."""
        elements = self.doc.cssselect("nav a.external")
        for element in elements:
            href = element.attrib["href"]
            if href.startswith("https://github.com"):
                return href

        return None

    @property
    def page_urls(self) -> List[str]:
        """URLs of all pages in a JupyterBook, selected from the ``<nav>``."""
        return [
            urljoin(self.html_page.url, link.attrib["href"])
            for link in self.doc.cssselect("nav a.internal")
            if link.attrib["href"] != "#"  # skip homepage
        ]

    @staticmethod
    def _clean_content(x: str) -> str:
        """Clean HTML content by removing extra newlines."""
        x = x.replace(r"\n", " ")
        x = x.replace("\n", " ")
        x = x.replace("\\", " ")
        x = x.strip()
        return x


class JupyterBookMetadata(BaseModel):
    """Metadata for a JupyterBook project.

    This metadata can be associated with individual page in a JupyterBook
    to give that page context.
    """

    root_url: HttpUrl
    """Root URL of the JupyterBook.

    The URL is validated to guarantee than it ends with a "/".
    """

    title: str
    """The title of the JupyterBook as a plain text string."""

    logo_url: HttpUrl
    """The URL of the JupyterBook's logo."""

    description: str
    """The description of the JupyterBook, extracted as the first content
    paragraph of the book.

    This string is unformatted (no HTML formatting).
    """

    source_repository: Optional[HttpUrl]
    """The URL of the book's source repository (i.e. GitHub repository)."""

    page_urls: List[HttpUrl]
    """URLs of pages in the JupyterBook."""

    @validator("root_url")
    def validate_root_url(cls, v: str) -> str:
        """Validate the root url so it points to a directory, not a "file"."""
        parsed_url = urlparse(v)
        path = "/".join(
            [p for p in parsed_url.path.split("/") if not p.endswith(".html")]
        )
        if not path.endswith("/"):
            path = f"{path}/"
        new_url = (
            parsed_url[0],
            parsed_url[1],
            path,
            "",  # un-set params
            "",  # un-set query
            "",  # un-set fragment
        )
        return urlunparse(new_url)
