# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Command-line interface for astropylibrarian."""

from __future__ import annotations

import typer

from astropylibrarian.cli import index

app = typer.Typer(
    short_help="Manage the content indexed by the Learn Astropy project."
)
app.add_typer(index.app, name="index")


@app.callback()
def main_callback() -> None:
    """Manage the content index for the Learn Astropy project.

    Astropy Librarian helps you work with the Algolia index that powers
    the content listing and search for Learn Astropy,
    https://learn.astropy.org.

    Astropy Librarian is developed at
    https://github.com/astropy/learn-astropy-librarian
    """
    typer.echo("I'm the main app callback.")


@app.command()
def delete() -> None:
    """Delete Algolia records."""
    typer.echo("I'm the delete command")
