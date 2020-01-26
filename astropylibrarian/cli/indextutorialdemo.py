# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Demonstration script that indexes a learn.astropy tutorial to Algolia.
"""

import argparse
import asyncio

from algoliasearch.search_client import SearchClient
import aiohttp


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Index a learn.astropy tutorial to Algolia."
    )
    parser.add_argument(
        'url',
        type=str,
        help='URL of the tutorial.')
    parser.add_argument(
        '--index',
        type=str,
        default='astropy_fulltext',
        help='Name of the index')
    parser.add_argument(
        '--env',
        type=str,
        choices=['dev', 'stage', 'prod'],
        default='dev',
        help='Environment suffix for index name')
    parser.add_argument(
        '--algolia-id',
        type=str,
        help='Algolia application ID')
    parser.add_argument(
        '--algolia-key',
        type=str,
        help='Algolia application key')
    return parser


def main() -> None:
    args = make_parser().parse_args()

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run(args=args))


async def run(args: argparse.Namespace) -> None:
    algolia_client = SearchClient.create(args.algolia_id, args.algolia_key)
    async with aiohttp.ClientSession() as http_client:
        print(f'Indexing {args.url}')
        await asyncio.sleep(1)
        print('Done')
