# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Workflow for indexing a learn.astropy tutorial to Algolia."""

from __future__ import annotations

__all__ = ["index_tutorial"]

import logging
from typing import TYPE_CHECKING, List

from astropylibrarian.algolia.client import generate_index_epoch
from astropylibrarian.reducers.tutorial import ReducedTutorial
from astropylibrarian.workflows.download import download_html
from astropylibrarian.workflows.expirerecords import expire_old_records

if TYPE_CHECKING:
    import aiohttp

    from astropylibrarian.client import AlgoliaIndexType

logger = logging.getLogger(__name__)


async def index_tutorial(
    *,
    url: str,
    http_client: aiohttp.ClientSession,
    algolia_index: AlgoliaIndexType,
) -> List[str]:
    """Asynchronously save records for a tutorial to Algolia (awaitable
    function).

    Parameters
    ----------
    url : `str`
        A URL for an HTML page.
    http_client : `aiohttp.ClientSession`
        An open aiohttp client.
    algolia_index
        Algolia index created by the
        `astropylibrarian.workflows.client.AlgoliaIndex` context manager.

    Returns
    -------
    object_ids : `list` of `str`
        List of Algolia record object IDs that are saved by this indexing
        operation.

    Notes
    -----
    Operations performed by this workflow:

    1. Download the HTML page
       (`~astropylibrarian.workflows.download.download_html`)
    2. Reduce the tutorial
       (~`astropylibrarian.reducers.tutorial.ReducedTutorial`)
    3. Create records for each section
       (`~astropylibrarian.algolia.records.TutorialSectionRecord`)
    4. Save each record to Algolia (`index.save_objects
       <https://www.algolia.com/doc/api-reference/api-methods/save-objects/>`_)
    """
    tutorial_html = await download_html(url=url, http_client=http_client)
    logger.debug("Downloaded %s", url)

    tutorial = ReducedTutorial(html_page=tutorial_html)

    index_epoch = generate_index_epoch()
    records = [
        r for r in tutorial.iter_algolia_objects(index_epoch=index_epoch)
    ]
    logger.debug("Indexing %d records for tutorial at %s", len(records), url)

    saved_object_ids: List[str] = []
    response = await algolia_index.save_objects_async(records)
    for r in response.raw_responses:
        _oids = r.get("objectIds", [])
        assert isinstance(_oids, list)
        saved_object_ids.extend(_oids)

    if saved_object_ids:
        await expire_old_records(
            algolia_index=algolia_index, root_url=url, index_epoch=index_epoch
        )

    return saved_object_ids
