# -*- coding: utf-8 -*-
"""Internal utility functions, not supposed to be used by the users."""
from copy import deepcopy
from typing import Set, Callable, Any, Iterable


def least_fixpoint(starting_set: Set, step: Callable[[Set], Iterable]) -> Set:
    """Do a least fixpoint algorithm."""
    z_current = None
    z_next = starting_set

    while z_current != z_next:
        z_current = z_next
        z_next = deepcopy(z_current)
        z_next = z_next.union(step(z_current))

    return z_current if z_current is not None else set()


def greatest_fixpoint(starting_set: Set, condition: Callable[[Any, Set], bool]) -> Set:
    """Do a greatest fixpoint algorithm."""
    z_current = None
    z_next = starting_set

    while z_current != z_next:
        z_current = z_next
        z_next = deepcopy(z_current)

        for e in z_current:
            if condition(e, z_current):
                z_next.remove(e)

    return z_current if z_current is not None else set()
