# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Command-line interface for astropylibrarian."""

from __future__ import annotations

import logging

import typer

from astropylibrarian.cli import index

app = typer.Typer(
    short_help="Manage the content indexed by the Learn Astropy project."
)
app.add_typer(index.app, name="index")


@app.callback()
def main_callback(
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help=(
            "Verbose output. Use -v for info-type logging and -vv for "
            "debug-level logging."
        ),
    )
) -> None:
    """Manage the content index for the Learn Astropy project.

    Astropy Librarian helps you work with the Algolia index that powers
    the content listing and search for Learn Astropy,
    https://learn.astropy.org.

    Astropy Librarian is developed at
    https://github.com/astropy/learn-astropy-librarian
    """
    if verbose == 0:
        logging_level = logging.WARN
    elif verbose == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.DEBUG

    if logging_level == logging.DEBUG:
        # Include the module name in the logging for easier debugging
        log_format = (
            "%(asctime)s %(levelname)8s %(name)s:%(lineno)d | %(message)s"
        )
    else:
        log_format = "%(levelname)s: %(message)s"

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(log_format, datefmt="%Y-%m-%d:%H:%M:%S")
    )
    logger = logging.getLogger("astropylibrarian")
    logger.addHandler(handler)
    logger.setLevel(logging_level)


@app.command()
def delete() -> None:
    """Delete Algolia records."""
    typer.echo("I'm the delete command")
