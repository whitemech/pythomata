# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Any

from pythomata.dfa import DFA, Symbol


class Simulator(ABC):

    @abstractmethod
    def make_transition(self, s: Symbol) -> Any:
        """Make a transition, updating the current state of the simulator."""

    @abstractmethod
    def is_true(self) -> bool:
        """Check if the simulator is in a final state."""

    @abstractmethod
    def word_acceptance(self, word: List[Symbol]) -> bool:
        """Check if a word is part of the language recognized by the automaton."""

    @abstractmethod
    def reset(self) -> Any:
        """Reset the state of the simulator to its initial state."""

    @abstractmethod
    def get_current_state(self):
        """Get the current state of the automaton."""


class DFASimulator(Simulator):
    """A DFA simulator."""

    def __init__(self, dfa: DFA):
        self.dfa = dfa.minimize()
        self.cur_state = self.dfa._initial_state

    def make_transition(self, s: Symbol):
        assert s in self.dfa._alphabet
        self.cur_state = self.dfa._idx_transition_function[self.cur_state][self.dfa._symbol_to_idx[s]]

    def is_true(self):
        return self.cur_state in self.dfa._idx_accepting_states

    def word_acceptance(self, word: List[Symbol]):
        self.reset()
        for s in word:
            self.make_transition(s)
        return self.is_true()

    def reset(self):
        self.cur_state = self.dfa._idx_initial_state

    def get_current_state(self):
        return self.cur_state
