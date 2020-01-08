#################
astropy-librarian
#################

The content crawler that supplies Astropy's web search.

Development primer
==================

Before developing astropy-librarian, set up a new Python virtual environment.
Then, install the application with development dependencies::

    pip install -e ".[dev]"

You can run the tests through Pytest_::

    pytest

In addition to running unit tests, ``pytest`` also lints the source with flake8_ and validates types with mypy_.

.. _Pytest: https://pytest.org/en/latest/
.. _mypy: https://mypy.readthedocs.io/en/latest/
.. _flake8: http://flake8.pycqa.org/en/latest/
