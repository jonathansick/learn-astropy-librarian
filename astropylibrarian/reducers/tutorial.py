# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Reduce the HTML source of a learn.astropy tutorial page (notebook-based)
into search records.
"""

__all__ = ('ReducedTutorial',)

from typing import List

import lxml.html

from .utils import iter_sphinx_sections, Section


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

    @property
    def sections(self) -> List[Section]:
        """The sections (`astropylibrarian.reducers.utils.Section`) that
        are found within the content.
        """
        return self._sections

    def __init__(self, *, html_source: str, url: str):
        self._url = url
        self._h1: str = ''
        self._authors: List[str] = []
        self._keywords: List[str] = []
        self._sections: List["Section"] = []
        self._process_html(html_source)

    def _process_html(self, html_source: str):
        doc = lxml.html.document_fromstring(html_source)

        self._h1 = self._get_section_title(doc.cssselect('h1')[0])

        authors_paragraph = doc.cssselect('.card .section p')[0]
        self._authors = self._parse_comma_list(authors_paragraph)

        keywords_paragraph = doc.cssselect('#keywords p')[0]
        self._keywords = self._parse_comma_list(keywords_paragraph)

        root_section = doc.cssselect('.card .section')[0]
        for s in iter_sphinx_sections(
                base_url=self._url,
                root_section=root_section,
                headers=[],
                header_callback=lambda x: x.rstrip('¶'),
                content_callback=lambda x: x.strip()):
            self._sections.append(s)
        # Also look for additional h1 section on the page.
        # Technically, the page should only have one h1, and all content
        # should be subsections of that. In real life, though, it's easy
        # to accidentally use additional h1 eleemnts for subsections.
        h1_heading = self._sections[-1].headings[-1]
        for sibling in root_section.itersiblings(tag='div'):
            if 'section' in sibling.classes:
                for s in iter_sphinx_sections(
                        root_section=sibling,
                        base_url=self._url,
                        headers=[h1_heading],
                        header_callback=lambda x: x.rstrip('¶'),
                        content_callback=lambda x: x.strip()
                        ):
                    self._sections.append(s)

    @staticmethod
    def _get_section_title(element: lxml.html.HtmlElement) -> str:
        return element.text_content().rstrip('¶')

    @staticmethod
    def _parse_comma_list(element: lxml.html.HtmlElement) -> List[str]:
        content = element.text_content()
        return [s.strip() for s in content.split(',')]
