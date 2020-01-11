# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Reduce the HTML source of a learn.astropy tutorial page (notebook-based)
into search records.
"""

__all__ = ('ReducedTutorial',)


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

    def __init__(self, *, html_source: str, url: str):
        self._url = url
