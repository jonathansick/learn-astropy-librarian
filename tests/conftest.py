"""Pytest configurations.
"""

from dataclasses import dataclass
from pathlib import Path

import pytest


@dataclass
class TestHtml:
    """A container for HTML pages cached in the repo's tests/data directory."""

    html: str
    """HTML content."""

    url: str
    """URL of the HTML content (in the real deployment)."""


@pytest.fixture(scope="session")
def color_excess_tutorial() -> TestHtml:
    """The color-excess.html tutorial page."""
    source_path = (
        Path(__file__).parent / "data" / "tutorials" / "color-excess.html"
    )
    return TestHtml(
        html=source_path.read_text(),
        url="http://learn.astropy.org/rst-tutorials/color-excess.html",
    )


@pytest.fixture(scope="session")
def coordinates_transform_tutorial() -> TestHtml:
    """The Coordinates-Transform.html tutorial page."""
    source_path = (
        Path(__file__).parent
        / "data"
        / "tutorials"
        / "Coordinates-Transform.html"
    )
    return TestHtml(
        html=source_path.read_text(),
        url="http://learn.astropy.org/rst-tutorials/"
        "Coordinates-Transform.html",
    )
