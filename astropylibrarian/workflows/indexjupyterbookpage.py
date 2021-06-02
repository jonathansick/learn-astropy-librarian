# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Workflow for ingesting a single page from a Jupyter Book site"""

from __future__ import annotations

__all__ = ["index_jupyterbook_page"]

from typing import TYPE_CHECKING, List

from astropylibrarian.reducers.jupyterbook import JupyterBookPage
from astropylibrarian.workflows.download import download_html

if TYPE_CHECKING:
    import aiohttp
    from algoliasearch.search_client import SearchClient

    from astropylibrarian.workflows.indexjupyterbook import JupyterBookMetadata


async def index_jupyterbook_page(
    *,
    url: str,
    jupyterbook_metadata: JupyterBookMetadata,
    http_client: aiohttp.ClientSession,
    algolia_client: SearchClient,
    index_name: str,
) -> List[str]:
    """Ingest a page from a JupyterBook site."""
    html_page = await download_html(url=url, http_client=http_client)
    page = JupyterBookPage(html_page)
    records = [
        record.dict(exclude_none=True)
        for record in page.iter_records(site_metadata=jupyterbook_metadata)
    ]
    index = algolia_client.init_index(index_name)
    response = await index.save_objects_async(records)
    print(response)

    object_ids = [r["object_id"] for r in records]
    return object_ids
