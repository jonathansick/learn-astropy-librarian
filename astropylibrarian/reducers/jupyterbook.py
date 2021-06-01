# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Reduce the HTML source of a JupyterBook-based Guide into search records."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, List, Optional
from urllib.parse import urljoin, urlparse, urlunparse

from pydantic import BaseModel, HttpUrl, validator

from astropylibrarian.reducers.utils import iter_sphinx_sections

if TYPE_CHECKING:
    import lxml.html

    from astropylibrarian.reducers.utils import Section
    from astropylibrarian.resources import HtmlPage


class JupyterBookPage:
    """A JupyterBook page, with accessors to key content."""

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

    def iter_sections(self) -> Iterator[Section]:
        """Iterate through sections in the page.

        Yields
        ------
        astropylibrarian.reducers.utils.Section
            A section of the document, which includes its content, heading
            hierarchy and anchor link.
        """
        root = self.doc.cssselect("#main-content .section")[0]
        for section in iter_sphinx_sections(
            root_section=root,
            base_url=self.html_page.url,
            headers=[],
            header_callback=lambda x: x.rstrip("¶"),
            content_callback=self._clean_content,
        ):
            yield section

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
