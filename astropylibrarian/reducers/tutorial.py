# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Reduce the HTML source of a learn.astropy tutorial page (notebook-based)
into search records.
"""

__all__ = ('ReducedTutorial',)

from typing import List

import lxml.html


class ReducedTutorial:
    """A reduction of a notebook-based learn.astropy tutorial page into search
    records.

    Parameters
    ----------
    html_source : str
        The HTML source of the tutorial page.
    url : str
        The canonical URL of the tutorial page.
    """

    @property
    def url(self) -> str:
        """The canonical URL of the tutorial page.
        """
        return self._url

    @property
    def h1(self) -> str:
        """The tutorial's H1 headline text.
        """
        return self._h1

    @property
    def authors(self) -> List[str]:
        """The names of authors declared by the tutorial page.
        """
        return self._authors

    @property
    def keywords(self) -> List[str]:
        """The keywords declared by the tutorial page.
        """
        return self._keywords

    def __init__(self, *, html_source: str, url: str):
        self._url = url
        self._h1: str = ''
        self._authors: List[str] = []
        self._keywords: List[str] = []
        self._process_html(html_source)

    def _process_html(self, html_source: str):
        doc = lxml.html.document_fromstring(html_source)

        self._h1 = self._get_section_title(doc.cssselect('h1')[0])

        authors_paragraph = doc.cssselect('.card .section p')[0]
        self._authors = self._parse_comma_list(authors_paragraph)

        keywords_paragraph = doc.cssselect('#keywords p')[0]
        self._keywords = self._parse_comma_list(keywords_paragraph)

    @staticmethod
    def _get_section_title(element: lxml.html.HtmlElement) -> str:
        return element.text_content().rstrip('¶')

    @staticmethod
    def _parse_comma_list(element: lxml.html.HtmlElement) -> List[str]:
        content = element.text_content()
        return [s.strip() for s in content.split(',')]
