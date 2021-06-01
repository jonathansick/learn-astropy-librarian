# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.reducers.jupyterbook module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astropylibrarian.reducers.jupyterbook import JupyterBookPage

if TYPE_CHECKING:
    from tests.conftest import HtmlTestData


def test_jupyterbookpage_sections(ccd_guide_01_05: HtmlTestData) -> None:
    page = JupyterBookPage(ccd_guide_01_05)
    sections = [s for s in page.iter_sections()]
    assert len(sections) > 0
