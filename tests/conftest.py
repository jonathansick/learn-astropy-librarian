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


@pytest.fixture(scope="session")
def ccd_guide_index() -> TestHtml:
    """The ``ccd-guide/index.html`` page.

    This page is the root file created by Jupyter Book, but which redirects
    to the first content page (notebooks/00-00-Preface.html).
    """
    source_path = Path(__file__).parent / "data" / "ccd-guide" / "index.html"
    return TestHtml(
        html=source_path.read_text(),
        url="http://www.astropy.org/ccd-reduction-and-photometry-guide/"
        "index.html",
    )


@pytest.fixture(scope="session")
def ccd_guide_00_00() -> TestHtml:
    """The ``ccd-guide/notebooks/00-00-Preface.html`` page.

    This is the CCD Guide homepage created by Jupyter Book.
    """
    source_path = (
        Path(__file__).parent
        / "data"
        / "ccd-guide"
        / "notebooks"
        / "00-00-Preface.html"
    )
    return TestHtml(
        html=source_path.read_text(),
        url="http://www.astropy.org/ccd-reduction-and-photometry-guide/"
        "notebooks/00-00-Preface.html",
    )


@pytest.fixture(scope="session")
def ccd_guide_01_05() -> TestHtml:
    """The ``ccd-guide/notebooks/01-05-Calibration-overview.html`` page.

    This is a regular content page from the CCD Guide homepage created by
    Jupyter Book.
    """
    source_path = (
        Path(__file__).parent
        / "data"
        / "ccd-guide"
        / "notebooks"
        / "01-05-Calibration-overview.html"
    )
    return TestHtml(
        html=source_path.read_text(),
        url="http://www.astropy.org/ccd-reduction-and-photometry-guide/"
        "notebooks/01-05-Calibration-overview.html",
    )
