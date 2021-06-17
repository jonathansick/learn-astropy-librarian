# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Workflow for deleting all Algolia records associated with a root URL."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from astropylibrarian.algolia.client import escape_facet_value

if TYPE_CHECKING:
    from typing import Any, AsyncIterator, Dict, List

    from astropylibrarian.algolia.client import AlgoliaIndexType

logger = logging.getLogger(__name__)


async def delete_root_url(
    *, root_url: str, algolia_index: AlgoliaIndexType
) -> List[str]:
    """Delete all Algolia records associated with a ``root_url``."""
    object_ids: List[str] = []
    async for record in search_for_records(
        index=algolia_index, root_url=root_url
    ):
        if record["root_url"] != root_url:
            logger.warning(
                "Search failure, root url of %s is %s",
                record["objectID"],
                record["root_url"],
            )
            continue
        object_ids.append(record["objectID"])

    logger.debug("Found %d objects for deletion", len(object_ids))

    response = await algolia_index.delete_objects_async(object_ids)
    logger.debug("Algolia response:\n%s", response.raw_responses)

    logger.info("Deleted %d objects", len(object_ids))

    return object_ids


async def search_for_records(
    *, index: AlgoliaIndexType, root_url: str
) -> AsyncIterator[Dict[str, Any]]:
    filters = f"root_url:{escape_facet_value(root_url)}"
    logger.debug("Filter:\n%s", filters)

    async for result in index.browse_objects_async(
        {
            "filters": filters,
            "attributesToRetrieve": ["root_url"],
            "attributesToHighlight": [],
        }
    ):
        yield result
