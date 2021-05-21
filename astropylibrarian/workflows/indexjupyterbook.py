# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Workflow for ingesting a Jupyter Book site (as a Learn Astropy Guide).

This workflow ingests the Jupyter Book homepage and triggers workflows to
ingest individual Jupyter Book content pages.
"""

from __future__ import annotations

__all__ = ["index_jupyterbook"]

import re
from typing import TYPE_CHECKING, List, Union
from urllib.parse import urljoin

from astropylibrarian.workflows.download import download_html

if TYPE_CHECKING:
    import aiohttp
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
    print(homepage)

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


def extract_page_urls(*, html_page: HtmlPage) -> List[str]:
    """Extract the page URLs form the ``<nav>`` element of a Jupyter Book page.

    Parameters
    ----------
    html_page : `astropylibrarian.resources.HtmlPage`
        The HTML page.

    Returns
    -------
    list of str
        List of page URLs, not including the homepage.
    """
    doc = html_page.parse()
    return [
        urljoin(html_page.url, link.attrib["href"])
        for link in doc.cssselect("nav a.internal")
        if link.attrib["href"] != "#"  # skip homepage
    ]
