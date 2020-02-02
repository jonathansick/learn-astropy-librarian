# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Record types that reflect Algolia search records.
"""

__all__ = ['TutorialSectionRecord']

from base64 import b64encode
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Any
from urllib.parse import urlparse, urlunparse

if TYPE_CHECKING:
    from astropylibrarian.reducers.utils import Section
    from astropylibrarian.reducers.tutorial import ReducedTutorial


@dataclass
class TutorialSectionRecord:
    """An Algolia record for learn.astropy tutorial sections.
    """

    section: 'Section'
    """The underlying Section content of the record
    (`astropylibrarian.reducers.utils.Section`).
    """

    tutorial: 'ReducedTutorial'
    """The reduced tutorial page that this record is associated with
    (`astropylibrarian.reducers.tutorial.ReducedTutorial`).
    """

    @property
    def object_id(self) -> str:
        """The objectID of the record.

        This is computed based on the URL and section heading hierarchy.
        """
        url_component = b64encode(
            self.section.url.lower().encode("utf-8")
        ).decode('utf-8')
        heading_component = b64encode(
            ' '.join(self.section.headings).encode("utf-8")
        ).decode('utf-8')
        return f'{url_component}-{heading_component}'

    @property
    def base_url(self) -> str:
        """The base URL of the tutorial that the section belongs to.

        This is the section's ``url`` attribute stripped of the fragment
        (``#id`` part).
        """
        url_parts = urlparse(self.section.url)
        return urlunparse((
            url_parts.scheme,
            url_parts.netloc,
            url_parts.path,
            '',
            '',
            ''
        ))

    @property
    def data(self) -> Dict[str, Any]:
        """The JSON-encodable record, ready for indexing by Algolia.
        """
        record = {
            'objectID': self.object_id,
            'baseUrl': self.base_url,
            'url': self.section.url,
            'content': self.section.content,
            'importance': self.section.header_level,
            'contentType': 'tutorial',
            'authors': self.tutorial.authors,
            'keywords': self.tutorial.keywords
        }
        for i, heading in enumerate(self.section.headings):
            record[f'h{i+1}'] = heading
        if self.tutorial.images:
            record['thumbnail'] = self.tutorial.images[0]
        return record
