"""Tests for the astropylibrarian.keywords module."""

from astropylibrarian.keywords import KeywordDb


def test_load() -> None:
    keyworddb = KeywordDb.load()
    assert isinstance(keyworddb, KeywordDb)


def test_get_astropy_package_keywords() -> None:
    inputs = [
        "astroquery",  # canonical keyword
        "astropy.coordinates",  # alternate form
        "numpy",  # not astropy package keyword
    ]
    outputs = ["astroquery", "coordinates"]

    keyworddb = KeywordDb.load()
    assert keyworddb.filter_keywords(inputs, "astropy_package") == outputs


def test_get_python_package_keywords() -> None:
    inputs = [
        "astroquery",  # wrong type
        "astropy.coordinates",  # wrong type
        "numpy",  # canonical keyword
    ]
    outputs = ["numpy"]

    keyworddb = KeywordDb.load()
    assert keyworddb.filter_keywords(inputs, "python_package") == outputs


def test_task_keywords() -> None:
    inputs = [
        "astroquery",  # wrong type
        "contour plots",  # canonical form
        "OOP",  # alternate form, also uppercase
    ]
    outputs = ["contour plots", "object-oriented programming"]

    keyworddb = KeywordDb.load()
    assert keyworddb.filter_keywords(inputs, "task") == outputs


def test_science_keywords() -> None:
    inputs = [
        "astroquery",  # wrong type
        "astrodynamics",
        "x-ray astronomy",
        "extinction",
    ]
    outputs = ["astrodynamics", "x-ray astronomy", "extinction"]

    keyworddb = KeywordDb.load()
    assert keyworddb.filter_keywords(inputs, "science") == outputs
