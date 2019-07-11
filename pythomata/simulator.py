# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Any, Optional

from pythomata.dfa import DFA, Symbol, State


class Simulator(ABC):

    @abstractmethod
    def step(self, s: Symbol) -> Any:
        """Make a transition, updating the current state of the simulator."""

    @abstractmethod
    def is_true(self) -> bool:
        """Check if the simulator is in a final state."""

    @abstractmethod
    def is_failed(self) -> bool:
        """Check if the simulator is failed (i.e. in an undefined state)."""

    @abstractmethod
    def reset(self) -> Any:
        """Reset the state of the simulator to its initial state."""


class DFASimulator(Simulator):
    """A DFA simulator."""

    def __init__(self, dfa: DFA):
        """
        Initialize a simulator for a DFA.
        
        :param dfa: the DFA. 
        """
        self.dfa = dfa
        self._cur_state = self.dfa.initial_state # type: Optional[State]
        self._is_failed = False  # type: bool

    @property
    def cur_state(self) -> Optional[State]:
        """
        The current state of the simulator.
        :return: the index corresponding to the automaton state.
               | If None, then the simulation is in a failure state.
        """
        return self._cur_state

    def step(self, s: Symbol):
        if self.is_failed() \
            or s not in self.dfa.alphabet \
            or s not in self.dfa.transition_function[self._cur_state]:
            self._is_failed = True
            self._cur_state = None
        else:
            self._cur_state = self.dfa.transition_function[self._cur_state][s]

    def is_true(self):
        return not self.is_failed() and self._cur_state in self.dfa.accepting_states

    def is_failed(self) -> bool:
        return self._is_failed

    def reset(self):
        self._is_failed = False
        self._cur_state = self.dfa.initial_state
