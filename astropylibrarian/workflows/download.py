# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Workflow for downloading an HTML page.
"""

__all__ = ["download_html"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import aiohttp


async def download_html(
    *, url: str, http_client: "aiohttp.ClientSession"
) -> str:
    """Asynchronously download an HTML page (awaitable function).

    Parameters
    ----------
    url : `str`
        A URL for an HTML page.
    http_client : `aiohttp.ClientSession`
        An open aiohttp client.

    Returns
    -------
    html_content : `str`
        The page's HTML.

    Raises
    ------
    DownloadError
        Raised if there is an error downloading a resource.
    """
    async with http_client.get(url) as resp:
        if resp.status != 200:
            raise DownloadError(f"url={url}")
        return await resp.text()


class DownloadError(RuntimeError):
    """Raised if there is an error downloading a resource."""
