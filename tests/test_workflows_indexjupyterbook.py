# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.workflows.indexjupyterbook module."""

from pathlib import Path
from typing import Union

import pytest

from astropylibrarian.workflows.indexjupyterbook import detect_redirect


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
