# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Standardized Learn Astropy keywords."""

from pathlib import Path
from typing import Dict, List, Optional

import yaml

KeywordTable = Dict[str, List[str]]
"""Keyword table data type.

The canonical keyword is the key, and alternative forms are strings in the
list.
"""


class KeywordDb:
    """A database of Astropy keywords and sorter of keyword types.

    Parameters
    ----------
    astropy_package : `KeywordTable`
        Keywords in the "Astropy package" group.
    python_package : `KeywordTable`
        Keywords in the "Python package" group.
    task : `KeywordTable`
        Keywords in the "task" group.
    science : `KeywordTable`
        Keywords in the "science" group.
    """

    def __init__(
        self, *, astropy_package: KeywordTable,
        python_package: KeywordTable, task: KeywordTable,
        science: KeywordTable
    ) -> None:
        self._astropy_package_keywords = astropy_package
        self._python_package_keywords = python_package
        self._task_keywords = task
        self._science_keywords = science

    @classmethod
    def load(cls, path: Optional[Path] = None) -> 'KeywordDb':
        """Load a KeywordDB from a YAML file.

        Parameters
        ----------
        path : `pathlib.Path`, optional
            Path to the YAML-formatted keyword database file. Leave as `None`
            to use the built-in keyword database.

        Returns
        -------
        KeywordDb
            A keyword database instance.
        """
        if path is None:
            path = Path(__file__).parent / 'data' / 'keywords.yaml'

        db = yaml.safe_load(path.read_text())

        astropy_package_keywords = cls._load_keyword_table(
            db['astropy_package'])
        python_package_keywords = cls._load_keyword_table(
            db['python_package'])
        task_keywords = cls._load_keyword_table(
            db['task'])
        science_keywords = cls._load_keyword_table(
            db['science'])

        return cls(
            astropy_package=astropy_package_keywords,
            python_package=python_package_keywords,
            task=task_keywords,
            science=science_keywords
        )

    @staticmethod
    def _load_keyword_table(group) -> KeywordTable:
        keywords = {}
        for keyword_item in group:
            if isinstance(keyword_item, dict):
                keyword = list(keyword_item.keys())[0]
                alternatives = keyword_item[keyword]
            elif isinstance(keyword_item, str):
                keyword = keyword_item
                alternatives = list()
            keywords[keyword] = alternatives
        return keywords

    def get_astropy_package_keywords(
            self, input_keywords: List[str]) -> List[str]:
        """Get the list of "Astropy package" type keywords from an input list
        of keywords that might include other type of keywords and alternate
        forms of keywords.
        """
        return self._get_keywords_in_table(
            table=self._astropy_package_keywords,
            input_keywords=input_keywords)

    def get_python_package_keywords(
            self, input_keywords: List[str]) -> List[str]:
        """Get the list of "Python package" type keywords from an input list
        of keywords that might include other type of keywords and alternate
        forms of keywords.
        """
        return self._get_keywords_in_table(
            table=self._python_package_keywords,
            input_keywords=input_keywords)

    def get_task_keywords(
            self, input_keywords: List[str]) -> List[str]:
        """Get the list of "task" type keywords from an input list
        of keywords that might include other type of keywords and alternate
        forms of keywords.
        """
        return self._get_keywords_in_table(
            table=self._task_keywords,
            input_keywords=input_keywords)

    def get_science_keywords(
            self, input_keywords: List[str]) -> List[str]:
        """Get the list of "science" type keywords from an input list
        of keywords that might include other type of keywords and alternate
        forms of keywords.
        """
        return self._get_keywords_in_table(
            table=self._science_keywords,
            input_keywords=input_keywords)

    def _get_keywords_in_table(self, *, table, input_keywords) -> List[str]:
        input_keywords = [k.lower().strip() for k in input_keywords]

        output_keywords: List[str] = []

        for input_keyword in input_keywords:
            if input_keyword in table.keys():
                # Keyword is in group and already the canonical form
                output_keywords.append(input_keyword)
            else:
                # See if the keyword is an alternative form
                for keyword, alternates in table.items():
                    if input_keyword in alternates:
                        output_keywords.append(keyword)

        return output_keywords
