# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.reducers.tutorial module.
"""

from astropylibrarian.reducers.tutorial import ReducedTutorial


def test_color_excess(color_excess_tutorial):
    """Test with the "color-excess.html" dataset.
    """
    reduced_tutorial = ReducedTutorial(
        html_source=color_excess_tutorial.html,
        url=color_excess_tutorial.url)

    assert reduced_tutorial.url == color_excess_tutorial.url
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
    assert reduced_tutorial.images[0] == (
        'http://learn.astropy.org/_images/color-excess_9_0.png'
    )
    assert reduced_tutorial.summary == (
        'In this tutorial, we will look at some extinction curves from the '
        'literature, use one of those curves to deredden an observed spectrum'
        ', and practice invoking a background source flux in order to '
        'calculate magnitudes from an extinction model.'
    )

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
