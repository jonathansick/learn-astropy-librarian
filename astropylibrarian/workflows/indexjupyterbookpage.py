# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Workflow for ingesting a single page from a Jupyter Book site"""

from __future__ import annotations

__all__ = ["index_jupyterbook_page"]

from typing import TYPE_CHECKING, List

from astropylibrarian.reducers.jupyterbook import JupyterBookPage
from astropylibrarian.workflows.download import download_html

if TYPE_CHECKING:
    import aiohttp

    from astropylibrarian.client import AlgoliaIndexType
    from astropylibrarian.workflows.indexjupyterbook import JupyterBookMetadata


async def index_jupyterbook_page(
    *,
    url: str,
    jupyterbook_metadata: JupyterBookMetadata,
    http_client: aiohttp.ClientSession,
    algolia_index: AlgoliaIndexType,
) -> List[str]:
    """Ingest a page from a JupyterBook site."""
    html_page = await download_html(url=url, http_client=http_client)
    page = JupyterBookPage(html_page)
    records = [
        record
        for record in page.iter_algolia_objects(
            site_metadata=jupyterbook_metadata
        )
    ]
    response = await algolia_index.save_objects_async(records)
    print(response)

    object_ids = [r["objectID"] for r in records]
    return object_ids
