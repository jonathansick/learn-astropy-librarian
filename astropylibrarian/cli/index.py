# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Astropy Librarian CLI "index" subcommand group."""

from __future__ import annotations

import typer

app = typer.Typer(short_help="Content indexing commands.")


@app.command()
def tutorial() -> None:
    """Index a single tutorial."""
    typer.echo("I'm the index tutorial command")


@app.command()
def guide() -> None:
    """Index a guide."""
    typer.echo("I'm the index guide command")
