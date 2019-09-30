# -*- coding: utf-8 -*-

"""Base module of the Pythomata package."""

from typing import Dict, Set, Hashable

SINK = "sink"
FORBIDDEN_STATE_SYMBOLS = {""}
FORBIDDEN_ALPHABET_SYMBOLS = {""}
Symbol = Hashable
State = Hashable
Alphabet = Set[Symbol]
TransitionFunction = Dict[State, Dict[Symbol, State]]
NondeterministicTransitionFunction = Dict[State, Dict[Symbol, Set[State]]]


class Sink(State):
    """Class to implement a sink state."""

    def __str__(self):
        """Get the string representation of the Sink object."""
        return "sink"

    def __eq__(self, other):
        """Check that the instance is equal to another object.

        In this case, this means comparing the type, since an instance of the Sink class
        is equal to any other instance.
        """
        return type(self) == type(other)

    def __hash__(self):
        """Compute the hash of the instance."""
        return hash(type(self))
