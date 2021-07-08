# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test the Algolia client and supporting code."""

import pytest

from astropylibrarian.algolia.client import escape_facet_value


@pytest.mark.parametrize(
    "value,expected",
    [
        ("https://learn.astropy.org/", '"https://learn.astropy.org/"'),
        ("O'clock", r'"O\'clock"'),
        ('"cool"', r'"\"cool\""'),
    ],
)
def test_escape_facet_value(value: str, expected: str) -> None:
    assert escape_facet_value(value) == expected
