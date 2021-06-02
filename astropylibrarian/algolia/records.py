# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Record types that reflect Algolia search records."""

from __future__ import annotations

__all__ = ["ContentType", "AlgoliaRecord", "TutorialRecord"]

import datetime
from base64 import b64encode
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from urllib.parse import urlparse, urlunparse

from pydantic import BaseModel, Field, HttpUrl, validator

if TYPE_CHECKING:
    from astropylibrarian.keywords import KeywordDb
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

    object_id: str = Field(description="Unique identifier for this record.")

    root_summary: Optional[str] = Field(
        description=(
            "Short summary of the content corresponding to the root_url."
        )
    )

    content_type: ContentType = Field(description="Content type.")

    url: HttpUrl = Field(
        description=(
            "The most-specific URL for this record. Compared to the base url "
            "this URL may contain things like fragments in the URL."
        ),
    )

    root_url: HttpUrl = Field(
        description=(
            "URL of the document project's root page. For multi-page sites "
            "this corresponds to the site's homepage. For single-page sites "
            "this corresponds to the page's URL and is the same as "
            "``baseUrl``."
        ),
    )

    root_title: str = Field(
        description=(
            "Title of the documentation project. For single-page sites "
            "This is the same as ``h1``."
        ),
    )

    base_url: HttpUrl = Field(
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
        description="Timestamp when the record was indexed.",
        default_factory=datetime.datetime.utcnow,
    )

    thumbnail_url: Optional[HttpUrl] = Field(
        description="URL of an image to use as a thumbnail.",
    )

    @staticmethod
    def compute_object_id_for_section(section: Section) -> str:
        """Compute an Algolia object ID given a content section.

        Parameters
        ----------
        section : `astropylibrarian.reducers.utils.Section`
            A content section.

        Returns
        -------
        str
            The object ID for an Algolia record.
        """
        url_component = b64encode(section.url.lower().encode("utf-8")).decode(
            "utf-8"
        )
        heading_component = b64encode(
            " ".join(section.headings).encode("utf-8")
        ).decode("utf-8")
        return f"{url_component}-{heading_component}"


class TutorialRecord(AlgoliaRecord):
    """A Pydantic model for a "tutorial" content type record."""

    authors: Optional[List[str]] = Field(description="List of author names.")

    astropy_package_keywords: Optional[List[str]] = Field(
        description="List of astropy package keywords.",
    )

    python_package_keywords: Optional[List[str]] = Field(
        description="List of python package keywords.",
    )

    task_keywords: Optional[List[str]] = Field(
        description="List of task keywords."
    )

    science_keywords: Optional[List[str]] = Field(
        description="List of science keywords."
    )

    content_type: ContentType = Field(
        description="Content type.", default=ContentType.tutorial
    )

    @validator("content_type")
    def validate_content_type(cls, v: Optional[str]) -> str:
        if v is None:
            return ContentType.tutorial
        elif v != ContentType.tutorial:
            raise ValueError("Content type must be `tutorial`.")
        return v

    @classmethod
    def from_section(
        cls,
        *,
        tutorial: ReducedTutorial,
        section: Section,
        keyworddb: KeywordDb,
    ) -> TutorialRecord:
        """Create a TutorialRecord from a reduced tutorial HTML page and
        specific section.

        Parameters
        ----------
        tutorial : astropylibrarian.reducers.tutorial.ReducedTutorial
            The tutorial.
        section : astropylibrarian.reducers.utils.Section
            A section of the tutorial, which corresponds 1:1 with an Algolia
            record.
        keyworddb : astropylibrarian.keywords.KeywordDb
            The keyword database to sort keywords in tutorials into
            categories for the Learn Astropy UI.

        Returns
        -------
        TutorialRecord
            A tutorial record, ready to index in Algolia.
        """
        base_url = cls.compute_base_url(tutorial=tutorial)
        kwargs: Dict[str, Any] = {
            "object_id": cls.compute_object_id_for_section(section),
            "url": section.url,
            "root_url": base_url,
            "root_title": tutorial.h1,
            "root_summary": tutorial.summary,
            "base_url": base_url,
            "importance": section.header_level,
            "content": section.content,
            "authors": tutorial.authors,
            "astropy_package_keywords": keyworddb.filter_keywords(
                tutorial.keywords, "astropy_package"
            ),
            "python_package_keywords": keyworddb.filter_keywords(
                tutorial.keywords, "python_package"
            ),
            "task_keywords": keyworddb.filter_keywords(
                tutorial.keywords, "task"
            ),
            "science_keywords": keyworddb.filter_keywords(
                tutorial.keywords, "science"
            ),
        }
        for i, heading in enumerate(section.headings):
            kwargs[f"h{i+1}"] = heading
        if tutorial.images:
            kwargs["thumbnail_url"] = tutorial.images[0]

        return cls(**kwargs)

    @staticmethod
    def compute_base_url(*, tutorial: ReducedTutorial) -> str:
        """The base URL of the tutorial that the section belongs to.

        This is the section's ``url`` attribute stripped of the fragment
        (``#id`` part).
        """
        url_parts = urlparse(tutorial.url)
        return urlunparse(
            (url_parts.scheme, url_parts.netloc, url_parts.path, "", "", "")
        )
