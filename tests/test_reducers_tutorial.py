# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.reducers.tutorial module.
"""

from pathlib import Path

from astropylibrarian.reducers.tutorial import ReducedTutorial


def test_color_excess():
    """Test with the "color-excess.html" dataset.
    """
    source_path = Path(__file__).parent / 'data' / 'tutorials' \
        / 'color-excess.html'
    source_html = source_path.read_text()
    canonical_url = 'http://learn.astropy.org/rst-tutorials/color-excess.html'
    reduced_tutorial = ReducedTutorial(
        html_source=source_html,
        url=canonical_url)

    assert reduced_tutorial.url == canonical_url
