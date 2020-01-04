# -*- coding: utf-8 -*-
"""This package contains Hypothesis strategies."""
from typing import List

from hypothesis.strategies import lists, dictionaries, booleans, sampled_from


def words(propositions: List[str], min_size=0, max_size=None):
    return lists(dictionaries(sampled_from(propositions), booleans()), min_size=min_size, max_size=max_size)
