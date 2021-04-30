# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.algolia.records module.
"""

from pathlib import Path

from astropylibrarian.algolia.records import TutorialSectionRecord
from astropylibrarian.reducers.tutorial import ReducedTutorial


def test_tutorialsectionrecord():
    source_path = Path(__file__).parent / 'data' / 'tutorials' \
        / 'color-excess.html'
    source_html = source_path.read_text()
    canonical_url = 'http://learn.astropy.org/rst-tutorials/color-excess.html'
    reduced_tutorial = ReducedTutorial(
        html_source=source_html,
        url=canonical_url)

    record = TutorialSectionRecord(
        section=reduced_tutorial.sections[0],
        tutorial=reduced_tutorial)

    assert record.base_url == canonical_url
    assert record.object_id == (
        'aHR0cDovL2xlYXJuLmFzdHJvcHkub3JnL3JzdC10dXRvcmlhbHMvY29sb3ItZXhjZXNz'
        'Lmh0bWwjbGVhcm5pbmctZ29hbHM=-QW5hbHl6aW5nIGludGVyc3RlbGxhciByZWRkZW5'
        'pbmcgYW5kIGNhbGN1bGF0aW5nIHN5bnRoZXRpYyBwaG90b21ldHJ5IExlYXJuaW5nIEd'
        'vYWxz'
    )
    assert record.data == {
        'objectID': record.object_id,
        'baseUrl': canonical_url,
        'url': f'{canonical_url}#learning-goals',
        'content': (
            'Investigate extinction curve shapes\n'
            'Deredden spectral energy distributions and spectra\n'
            'Calculate photometric extinction and reddening\n'
            'Calculate synthetic photometry for a dust-reddened star by '
            'combining\ndust_extinction and synphot\n'
            'Convert from frequency to wavelength with astropy.unit\n'
            'equivalencies\n'
            'Unit support for plotting with astropy.visualization'
        ),
        'importance': 2,
        'authors': [
            'Kristen Larson',
            'Lia Corrales',
            'Stephanie T. Douglas',
            'Kelle Cruz'],
        'contentType': 'tutorial',
        'keywords': [
            'dust extinction',
            'synphot',
            'astroquery',
            'units',
            'photometry',
            'extinction',
            'physics',
            'observational astronomy'],
        'h1': ("Analyzing interstellar reddening and calculating synthetic "
               "photometry"),
        'h2': 'Learning Goals',
        'thumbnail': 'http://learn.astropy.org/_images/color-excess_9_0.png'
    }
