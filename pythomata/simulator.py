# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Any

from pythomata.dfa import DFA, Symbol


class Simulator(ABC):

    @abstractmethod
    def step(self, s: Symbol) -> Any:
        """Make a transition, updating the current state of the simulator."""

    @abstractmethod
    def is_true(self) -> bool:
        """Check if the simulator is in a final state."""

    @abstractmethod
    def accepts(self, word: List[Symbol]) -> bool:
        """Check if a word is part of the language recognized by the automaton."""

    @abstractmethod
    def reset(self) -> Any:
        """Reset the state of the simulator to its initial state."""


class DFASimulator(Simulator):
    """A DFA simulator."""

    def __init__(self, dfa: DFA):
        self.dfa = dfa.minimize()
        self.cur_state = self.dfa._initial_state

    def step(self, s: Symbol):
        try:
            assert s in self.dfa._alphabet
        except AssertionError:
            raise ValueError("Symbol '{}' not in the alphabet of the DFA.".format(s))
        self.cur_state = self.dfa._idx_transition_function[self.cur_state][self.dfa._symbol_to_idx[s]]

    def is_true(self):
        return self.cur_state in self.dfa._idx_accepting_states

    def accepts(self, word: List[Symbol]) -> bool:
        return self.dfa.accepts(word)

    def reset(self):
        self.cur_state = self.dfa._idx_initial_state
