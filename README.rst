#######################
learn-astropy-librarian
#######################

The content crawler that supplies Learn Astropy's web search.

Development primer
==================

Before developing learn-astropy-librarian, set up a new Python virtual environment.
Then, install the application with development dependencies::

    make init

This command installs pre-commit hooks for code linting, installs tox, resets the tox environment, and installs the package itself.

You can run all tests through tox_::

    tox

You can also run tox environments individually:

- ``tox -e py`` runs unit tests with Pytest_.
- ``tox -e lint`` runs code linters (such as flake8_ and pre-commit_).
- ``tox -e typing`` runs mypy_ to check type annotations.

.. _Pytest: https://pytest.org/en/latest/
.. _mypy: https://mypy.readthedocs.io/en/latest/
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _pre-commit: https://pre-commit.com
