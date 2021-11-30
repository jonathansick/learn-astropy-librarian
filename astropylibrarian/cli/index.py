# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Astropy Librarian CLI "index" subcommand group."""

from __future__ import annotations

import asyncio

import aiohttp
import typer

from astropylibrarian.algolia.client import AlgoliaIndex
from astropylibrarian.workflows.indexjupyterbook import index_jupyterbook
from astropylibrarian.workflows.indextutorial import index_tutorial_from_url

app = typer.Typer(short_help="Content indexing commands.")


@app.command()
def tutorial(
    url: str = typer.Argument(..., help="URL for a tutorial."),
    algolia_id: str = typer.Option(
        ..., help="Algolia app ID.", envvar="ALGOLIA_ID"
    ),
    algolia_key: str = typer.Option(
        ...,
        help="Algolia API key.",
        envvar="ALGOLIA_KEY",
        prompt=True,
        confirmation_prompt=False,
        hide_input=True,
    ),
    index: str = typer.Option(
        ..., help="Name of the Algolia index.", envvar="ALGOLIA_INDEX"
    ),
    priority: int = typer.Option(
        0,
        help="Priority for default sorting (higher numbers appear first)",
    ),
) -> None:
    """Index a single tutorial."""
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        run_index_tutorial(
            url=url,
            algolia_id=algolia_id,
            algolia_key=algolia_key,
            index=index,
            priority=priority,
        )
    )


async def run_index_tutorial(
    *, url: str, algolia_id: str, algolia_key: str, index: str, priority: int
) -> None:
    async with aiohttp.ClientSession() as http_client:
        async with AlgoliaIndex(
            key=algolia_key, app_id=algolia_id, name=index
        ) as algolia_index:
            await index_tutorial_from_url(
                url=url,
                http_client=http_client,
                algolia_index=algolia_index,
                priority=priority,
            )


@app.command()
def guide(
    url: str = typer.Argument(..., help="Root URL for a guide."),
    algolia_id: str = typer.Option(
        ..., help="Algolia app ID.", envvar="ALGOLIA_ID"
    ),
    algolia_key: str = typer.Option(
        ...,
        help="Algolia API key.",
        envvar="ALGOLIA_KEY",
        prompt=True,
        confirmation_prompt=False,
        hide_input=True,
    ),
    index: str = typer.Option(
        ..., help="Name of the Algolia index.", envvar="ALGOLIA_INDEX"
    ),
    priority: int = typer.Option(
        0,
        help="Priority for default sorting (higher numbers appear first)",
    ),
) -> None:
    """Index a guide."""
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        run_index_guide(
            url=url,
            algolia_id=algolia_id,
            algolia_key=algolia_key,
            index=index,
            priority=priority,
        )
    )


async def run_index_guide(
    *, url: str, algolia_id: str, algolia_key: str, index: str, priority: int
) -> None:
    async with aiohttp.ClientSession() as http_client:
        async with AlgoliaIndex(
            key=algolia_key, app_id=algolia_id, name=index
        ) as algolia_index:
            await index_jupyterbook(
                url=url,
                http_client=http_client,
                algolia_index=algolia_index,
                priority=priority,
            )
