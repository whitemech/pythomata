# -*- coding: utf-8 -*-
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

    def __str__(self):
        return "sink"

    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return hash(type(self))
