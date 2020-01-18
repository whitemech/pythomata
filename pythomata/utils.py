# -*- coding: utf-8 -*-
"""Utils module."""
from itertools import chain, combinations


def iter_powerset(iterable):
    """Get the powerset of an iterable, as an iterator."""
    s = set(iterable)
    combs = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
    return combs


def powerset(iterable):
    """
    Compute the power set of an iterable object.

    >>> sorted([sorted(s) for s in powerset([1,2,3])])
    [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    """
    combs = iter_powerset(iterable)
    res = set(frozenset(x) for x in combs)
    return res
