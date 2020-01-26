# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Workflow for indexing a learn.astropy tutorial to Algolia.
"""

__all__ = ['index_tutorial']

from typing import TYPE_CHECKING, List

from astropylibrarian.reducers.tutorial import ReducedTutorial
from astropylibrarian.algolia.records import TutorialSectionRecord
from .download import download_html

if TYPE_CHECKING:
    import aiohttp
    from algoliasearch.search_client import SearchClient


async def index_tutorial(
        *,
        url: str,
        http_client: 'aiohttp.ClientSession',
        algolia_client: 'SearchClient',
        index_name: str) -> List[str]:
    """Asynchronously save records for a tutorial to Algolia (awaitable
    function).

    Parameters
    ----------
    url : `str`
        A URL for an HTML page.
    http_client : `aiohttp.ClientSession`
        An open aiohttp client.
    algolia_client : `algoliasearch.search_client.SearchClient`
        The Algolia client.
    index_name : `str`
        The full name of the Algolia index to save the records to.

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
    print(f'Downloaded {url}')

    tutorial = ReducedTutorial(html_source=tutorial_html, url=url)

    records = [TutorialSectionRecord(section=s, tutorial=tutorial)
               for s in tutorial.sections]
    record_objects = [r.data for r in records]
    print(f'Indexing {len(record_objects)} objects')

    index = algolia_client.init_index(index_name)
    index.save_objects(record_objects).wait()

    # TODO Next step is to search for existing records about this URL
    # and delete and records that don't exist in the present record listing
    # because they're old content.

    saved_object_ids = [r.object_id for r in records]
    return saved_object_ids
