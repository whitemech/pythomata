# -*- coding: utf-8 -*-
"""This package contains Hypothesis strategies."""
from typing import Sequence

from hypothesis.strategies import lists, dictionaries, booleans, sampled_from


def simple_words(symbols: Sequence[str], min_size=0, max_size=None):
    return lists(sampled_from(symbols), min_size=min_size, max_size=max_size)


def propositional_words(propositions: Sequence[str], min_size=0, max_size=None):
    return lists(
        dictionaries(sampled_from(propositions), booleans()),
        min_size=min_size,
        max_size=max_size,
    )
