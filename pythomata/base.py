from typing import Dict, Tuple, Set

SINK = "sink"
FORBIDDEN_STATE_SYMBOLS = {""}
FORBIDDEN_ALPHABET_SYMBOLS = {""}
Symbol = str
State = str
Alphabet = Set[Symbol]
TransitionFunction = Dict[Tuple[State, Symbol], State]


class Sink(object):
    def __str__(self):
        return "sink"

    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return hash(type(self))
