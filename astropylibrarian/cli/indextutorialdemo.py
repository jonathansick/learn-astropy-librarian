# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Demonstration script that indexes a learn.astropy tutorial to Algolia.
"""

import argparse
import asyncio
import logging

from algoliasearch.search_client import SearchClient
import aiohttp

from astropylibrarian.workflows.indextutorial import index_tutorial


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
    parser.add_argument(
        '-l', '--log-level',
        choices=['debug', 'info', 'warn', 'error'],
        default='info',
        help='Logging level')
    return parser


def configure_logging(log_level: str) -> None:
    """Set up with logging format and level."""
    log_level = log_level.upper()
    if log_level == "DEBUG":
        # Include the module name in the logging for easier debugging
        log_format = "%(asctime)s %(levelname)8s $(name)s | %(message)s"
    else:
        log_format = "%(levelname)s: %(message)s"
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format))
    logger = logging.getLogger("astropylibrarian")
    logger.addHandler(handler)
    logger.setLevel(log_level)


def main() -> None:
    args = make_parser().parse_args()

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run(args=args))


async def run(args: argparse.Namespace) -> None:
    configure_logging(args.log_level)
    logger = logging.getLogger(__name__)
    algolia_client = SearchClient.create(args.algolia_id, args.algolia_key)
    async with aiohttp.ClientSession() as http_client:
        logger.info('Indexing %s', args.url)
        await index_tutorial(
            url=args.url,
            http_client=http_client,
            algolia_client=algolia_client,
            index_name=f'{args.index}_{args.env}'
        )
        logger.info('Done')
