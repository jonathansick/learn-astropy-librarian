# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.workflows.indexjupyterbook module."""

from __future__ import annotations

from typing import Union

import pytest

from astropylibrarian.workflows.indexjupyterbook import (
    detect_redirect,
    extract_page_urls,
)

from .conftest import HtmlTestData


@pytest.mark.parametrize(
    "html_path,base_url,expected",
    [
        (
            "ccd-guide/index.html",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/"
            "notebooks/00-00-Preface.html",
        ),
        (
            "ccd-guide/index.html",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/"
            "index.html",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/"
            "notebooks/00-00-Preface.html",
        ),
        (
            "ccd-guide/notebooks/00-00-Preface.html",
            "https://www.astropy.org/ccd-reduction-and-photometry-guide/"
            "index.html",
            None,
        ),
    ],
)
def test_detect_redirect(
    html_path: str, base_url: str, expected: Union[None, str]
) -> None:
    html_page = HtmlTestData.from_path(path=html_path, url=base_url)
    assert expected == detect_redirect(html_page)


def test_extract_page_urls(ccd_guide_00_00: HtmlTestData) -> None:
    extracted = extract_page_urls(html_page=ccd_guide_00_00)
    assert (
        "http://www.astropy.org/ccd-reduction-and-photometry-guide/notebooks/"
        "01-00-Understanding-an-astronomical-CCD-image.html"
    ) in extracted
