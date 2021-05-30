# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Record types that reflect Algolia search records.
"""

__all__ = ["TutorialSectionRecord"]

import datetime
from base64 import b64encode
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from urllib.parse import urlparse, urlunparse

from pydantic import BaseModel, Field, HttpUrl

from astropylibrarian.keywords import KeywordDb

if TYPE_CHECKING:
    from astropylibrarian.reducers.tutorial import ReducedTutorial
    from astropylibrarian.reducers.utils import Section


class ContentType(str, Enum):
    """Learn Astropy content types."""

    tutorial = "tutorial"

    guide = "guide"

    example = "example"

    documentation = "documentation"


class AlgoliaRecord(BaseModel):
    """A Pydantic model for an Learn Astropy record in Algolia."""

    object_id: str = Field(
        alias="objectID", description="Unique identifier for this record."
    )

    content_type: ContentType = Field(
        alias="contentType", description="Content type."
    )

    root_url: HttpUrl = Field(
        alias="rootUrl",
        description=(
            "URL of the document project's root page. For multi-page sites "
            "this corresponds to the site's homepage. For single-page sites "
            "this corresponds to the page's URL and is the same as "
            "``baseUrl``."
        ),
    )

    root_title: str = Field(
        alias="rootTitle",
        description=(
            "Title of the documentation project. For single-page sites "
            "This is the same as ``h1``."
        ),
    )

    base_url: HttpUrl = Field(
        alias="baseUrl",
        description=(
            "The base URL of the page, without fragments, parameters, "
            "queries, etc."
        ),
    )

    h1: str = Field(description="The title.")

    h2: Optional[str] = Field(description="The second-level heading.")

    h3: Optional[str] = Field(description="The third-level heading.")

    h4: Optional[str] = Field(description="The fourth-level heading.")

    h5: Optional[str] = Field(description="The fifth-level heading.")

    h6: Optional[str] = Field(description="The sixth-level heading.")

    importance: int = Field(
        description="The importance of the record, corresponding to the "
        "hierarchical section level"
    )

    content: str = Field(description="The plain text content of the record.")

    date_indexed: datetime.datetime = Field(
        alias="dateIndexed",
        description="Timestamp when the record was indexed.",
        default_factory=datetime.datetime.utcnow,
    )

    thumbnail_url: Optional[HttpUrl] = Field(
        alias="thumbnailUrl",
        description="URL of an image to use as a thumbnail.",
    )


@dataclass
class TutorialSectionRecord:
    """An Algolia record for learn.astropy tutorial sections."""

    section: "Section"
    """The underlying Section content of the record
    (`astropylibrarian.reducers.utils.Section`).
    """

    tutorial: "ReducedTutorial"
    """The reduced tutorial page that this record is associated with
    (`astropylibrarian.reducers.tutorial.ReducedTutorial`).
    """

    keyworddb: KeywordDb = field(default_factory=KeywordDb.load)
    """Keyword database."""

    @property
    def object_id(self) -> str:
        """The objectID of the record.

        This is computed based on the URL and section heading hierarchy.
        """
        url_component = b64encode(
            self.section.url.lower().encode("utf-8")
        ).decode("utf-8")
        heading_component = b64encode(
            " ".join(self.section.headings).encode("utf-8")
        ).decode("utf-8")
        return f"{url_component}-{heading_component}"

    @property
    def base_url(self) -> str:
        """The base URL of the tutorial that the section belongs to.

        This is the section's ``url`` attribute stripped of the fragment
        (``#id`` part).
        """
        url_parts = urlparse(self.section.url)
        return urlunparse(
            (url_parts.scheme, url_parts.netloc, url_parts.path, "", "", "")
        )

    @property
    def astropy_package_keywords(self) -> List[str]:
        """The list of "Astropy package" keywords."""
        return self.keyworddb.filter_keywords(
            self.tutorial.keywords, "astropy_package"
        )

    @property
    def python_package_keywords(self) -> List[str]:
        """The list of "Python package" keywords."""
        return self.keyworddb.filter_keywords(
            self.tutorial.keywords, "python_package"
        )

    @property
    def task_keywords(self) -> List[str]:
        """The list of "task" keywords."""
        return self.keyworddb.filter_keywords(self.tutorial.keywords, "task")

    @property
    def science_keywords(self) -> List[str]:
        """The list of "science" keywords."""
        return self.keyworddb.filter_keywords(
            self.tutorial.keywords, "science"
        )

    @property
    def data(self) -> Dict[str, Any]:
        """The JSON-encodable record, ready for indexing by Algolia."""
        record = {
            "objectID": self.object_id,
            "baseUrl": self.base_url,
            "url": self.section.url,
            "content": self.section.content,
            "importance": self.section.header_level,
            "contentType": "tutorial",
            "authors": self.tutorial.authors,
            "astropy_package_keywords": self.astropy_package_keywords,
            "python_package_keywords": self.python_package_keywords,
            "task_keywords": self.task_keywords,
            "science_keywords": self.science_keywords,
            "dateIndexed": f"{datetime.datetime.now().isoformat()}Z",
        }
        for i, heading in enumerate(self.section.headings):
            record[f"h{i+1}"] = heading
        if self.tutorial.images:
            record["thumbnail"] = self.tutorial.images[0]
        return record
