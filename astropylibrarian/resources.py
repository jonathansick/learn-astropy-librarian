# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Basic APIs for dealing with resources on the web, such as web pages."""

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

import lxml.html


@dataclass
class HtmlPage:
    """A representation of an HTML page and its context on the web."""

    html: str
    """The HTML content."""

    url: str
    """The URL that this page was downloaded from (which might be different
    from the ``request_url``).

    This URL is considered to be the "canonical URL."
    """

    request_url: Optional[str] = None
    """The URL that was originally requested to obtain this page, which might
    be different than the ``url`` if the server redirected.
    """

    headers: Mapping[str, Any] = field(default_factory=dict)
    """The HTTP response headers."""

    def parse(self) -> lxml.html.HtmlElement:
        """Parse the HTML content with ``lxml.html``."""
        return lxml.html.document_fromstring(self.html)
