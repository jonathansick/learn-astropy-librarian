# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.algolia.records module."""

from __future__ import annotations

import datetime
import json
from typing import TYPE_CHECKING

from astropylibrarian.reducers.tutorial import ReducedTutorial

if TYPE_CHECKING:
    from .conftest import HtmlTestData


def test_tutorialsectionrecord(color_excess_tutorial: HtmlTestData) -> None:
    reduced_tutorial = ReducedTutorial(html_page=color_excess_tutorial)

    records = [r for r in reduced_tutorial.iter_records()]
    record = records[0]

    assert record.base_url == color_excess_tutorial.url
    assert record.object_id == (
        "aHR0cDovL2xlYXJuLmFzdHJvcHkub3JnL3JzdC10dXRvcmlhbHMvY29sb3ItZXhjZXNz"
        "Lmh0bWwjbGVhcm5pbmctZ29hbHM=-QW5hbHl6aW5nIGludGVyc3RlbGxhciByZWRkZW5"
        "pbmcgYW5kIGNhbGN1bGF0aW5nIHN5bnRoZXRpYyBwaG90b21ldHJ5IExlYXJuaW5nIEd"
        "vYWxz"
    )
    data = json.loads(record.json(exclude_none=True))

    # Get the indexedDatetime field out because it's dynamic
    indexed_datetime = data.pop("date_indexed")
    # Ensure it's formatted correctly
    datetime.datetime.strptime(indexed_datetime, "%Y-%m-%dT%H:%M:%S.%f")

    # Ensure that the structure of other sections matches the expectation
    assert data == {
        "object_id": record.object_id,
        "root_url": color_excess_tutorial.url,
        "root_title": reduced_tutorial.h1,
        "base_url": color_excess_tutorial.url,
        "url": f"{color_excess_tutorial.url}#learning-goals",
        "content": (
            "Investigate extinction curve shapes "
            "Deredden spectral energy distributions and spectra "
            "Calculate photometric extinction and reddening "
            "Calculate synthetic photometry for a dust-reddened star by "
            "combining dust_extinction and synphot "
            "Convert from frequency to wavelength with astropy.unit "
            "equivalencies "
            "Unit support for plotting with astropy.visualization"
        ),
        "importance": 2,
        "authors": [
            "Kristen Larson",
            "Lia Corrales",
            "Stephanie T. Douglas",
            "Kelle Cruz",
        ],
        "content_type": "tutorial",
        "astropy_package_keywords": [
            "dust_extinction",
            "synphot",
            "astroquery",
            "units",
        ],
        "python_package_keywords": [],
        "task_keywords": [
            "photometry",
        ],
        "science_keywords": [
            "extinction",
            "physics",
            "observational astronomy",
        ],
        "h1": (
            "Analyzing interstellar reddening and calculating synthetic "
            "photometry"
        ),
        "h2": "Learning Goals",
        "thumbnail_url": (
            "http://learn.astropy.org/_images/color-excess_9_0.png"
        ),
    }
