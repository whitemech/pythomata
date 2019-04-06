# -*- coding: utf-8 -*-
from itertools import chain, combinations


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(set(iterable))
    combs = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    res = set(frozenset(x) for x in combs)
    # res = map(frozenset, combs)
    return res
