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
    assert reduced_tutorial.h1 == (
        'Analyzing interstellar reddening and calculating synthetic photometry'
    )
    assert reduced_tutorial.authors == [
        'Kristen Larson',
        'Lia Corrales',
        'Stephanie T. Douglas',
        'Kelle Cruz'
    ]
    assert reduced_tutorial.keywords == [
        'dust extinction',
        'synphot',
        'astroquery',
        'units',
        'photometry',
        'extinction',
        'physics',
        'observational astronomy'
    ]

    assert reduced_tutorial.sections[0].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Learning Goals"
    ]
    assert reduced_tutorial.sections[1].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Keywords"
    ]
    assert reduced_tutorial.sections[2].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Companion Content"
    ]
    assert reduced_tutorial.sections[3].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Summary"
    ]
    assert reduced_tutorial.sections[4].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry"
    ]
    assert reduced_tutorial.sections[5].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Introduction"
    ]
    assert reduced_tutorial.sections[6].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Example 1: Investigate Extinction Models"
    ]
    assert reduced_tutorial.sections[7].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Example 2: Deredden a Spectrum"
    ]
    assert reduced_tutorial.sections[8].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Example 3: Calculate Color Excess with synphot",
        "Exercise"
    ]
    assert reduced_tutorial.sections[9].headings == [
        "Analyzing interstellar reddening and calculating synthetic "
        "photometry",
        "Example 3: Calculate Color Excess with synphot"
    ]
