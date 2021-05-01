# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the astropylibrarian.algolia.records module.
"""

import datetime

from astropylibrarian.algolia.records import TutorialSectionRecord
from astropylibrarian.reducers.tutorial import ReducedTutorial


def test_tutorialsectionrecord(color_excess_tutorial):
    reduced_tutorial = ReducedTutorial(
        html_source=color_excess_tutorial.html,
        url=color_excess_tutorial.url)

    record = TutorialSectionRecord(
        section=reduced_tutorial.sections[0],
        tutorial=reduced_tutorial)

    assert record.base_url == color_excess_tutorial.url
    assert record.object_id == (
        'aHR0cDovL2xlYXJuLmFzdHJvcHkub3JnL3JzdC10dXRvcmlhbHMvY29sb3ItZXhjZXNz'
        'Lmh0bWwjbGVhcm5pbmctZ29hbHM=-QW5hbHl6aW5nIGludGVyc3RlbGxhciByZWRkZW5'
        'pbmcgYW5kIGNhbGN1bGF0aW5nIHN5bnRoZXRpYyBwaG90b21ldHJ5IExlYXJuaW5nIEd'
        'vYWxz'
    )
    data = record.data

    # Get the indexedDatetime field out because it's dynamic
    indexed_datetime = data.pop('dateIndexed')
    # Ensure it's formatted correctly
    datetime.datetime.strptime(indexed_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Ensure that the structure of other sections matches the expectation
    assert data == {
        'objectID': record.object_id,
        'baseUrl': color_excess_tutorial.url,
        'url': f'{color_excess_tutorial.url}#learning-goals',
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
