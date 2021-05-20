# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.workflows.indexjupyterbook module."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Union

import pytest

from astropylibrarian.workflows.indexjupyterbook import (
    detect_redirect,
    extract_page_urls,
)

if TYPE_CHECKING:
    from conftest import TestHtml


@pytest.mark.parametrize(
    "html_path,base_url,expected",
    [
        (
            "data/ccd-guide/index.html",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/"
            "notebooks/00-00-Preface.html",
        ),
        (
            "data/ccd-guide/index.html",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/"
            "index.html",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/"
            "notebooks/00-00-Preface.html",
        ),
        (
            "data/ccd-guide/notebooks/00-00-Preface.html",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/"
            "index.html",
            None,
        ),
    ],
)
def test_detect_redirect(
    html_path: str, base_url: str, expected: Union[None, str]
) -> None:
    html = Path(__file__).parent.joinpath(html_path).read_text()
    assert expected == detect_redirect(html=html, url=base_url)


def test_extract_page_urls(ccd_guide_00_00: TestHtml) -> None:
    extracted = extract_page_urls(
        html=ccd_guide_00_00.html, url=ccd_guide_00_00.url
    )
    assert (
        "http://www.astropy.org/ccd-reduction-and-photometry-guide/notebooks/"
        "01-00-Understanding-an-astronomical-CCD-image.html"
    ) in extracted
