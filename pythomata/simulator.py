# -*- coding: utf-8 -*-
"""This module contains implements utilities to execute a finite automaton."""
from abc import ABC, abstractmethod
from functools import reduce
from typing import Generic, Set, AbstractSet, Sequence

from pythomata.core import StateType, SymbolType, FiniteAutomaton


class AbstractSimulator(Generic[StateType, SymbolType], ABC):
    """An interface for a simulator of finite automata."""

    @abstractmethod
    def step(self, s: SymbolType) -> AbstractSet[StateType]:
        """Make a transition, updating the current state of the simulator."""

    @property
    @abstractmethod
    def is_started(self) -> bool:
        """Check if the simulator has been already started."""

    @abstractmethod
    def is_true(self) -> bool:
        """Check if the simulator is in a final state."""

    @abstractmethod
    def is_failed(self) -> bool:
        """Check if the simulator is failed (i.e. in an undefined state)."""

    @abstractmethod
    def reset(self) -> AbstractSet[StateType]:
        """Reset the state of the simulator to its initial state."""

    @abstractmethod
    def accepts(self, subword: Sequence[SymbolType]) -> bool:
        """Check whether the subword is accepted from the current state of the simulator."""


class AutomatonSimulator(AbstractSimulator[StateType, SymbolType]):
    """
    A concrete simulator for automaton.

    This class implements useful methods to simulate a behaviour of an automaton.
    It keeps the state
    """

    def __init__(self, automaton: FiniteAutomaton):
        """
        Initialize a simulator for a finite automaton.

        :param automaton: the automaton.
        """
        self._automaton = automaton
        self._is_started = False  # type: bool
        self._current_states = {
            self._automaton.initial_state
        }  # type: AbstractSet[StateType]

    @property
    def automaton(self) -> FiniteAutomaton:
        """Get the automaton."""
        return self._automaton

    @property
    def is_started(self) -> bool:
        """Check if the simulator has been already started."""
        return self._is_started

    @property
    def cur_state(self) -> AbstractSet[StateType]:
        """
        Get the current states of the simulator.

        :return: the index corresponding to the automaton state.
               | If empty, then the simulation is in a failure state.
        """
        return self._current_states

    def step(self, symbol: SymbolType) -> AbstractSet[StateType]:
        """Do a simulation step."""
        self._is_started = True
        next_macro_state = set()  # type: Set[StateType]
        for state in self.cur_state:
            next_macro_state = next_macro_state.union(
                self.automaton.get_successors(state, symbol)
            )
        self._current_states = next_macro_state
        return next_macro_state

    def is_true(self) -> bool:
        """Check whether the simulator is in an accepting state."""
        return not self.is_failed() and any(
            s in self.automaton.accepting_states for s in self.cur_state
        )

    def is_failed(self) -> bool:
        """Check whether the simulator is in a failed state."""
        return self.cur_state == set()

    def reset(self) -> AbstractSet[StateType]:
        """Reset the simulator."""
        self._current_states = {self.automaton.initial_state}
        self._is_started = False
        return self.cur_state

    def accepts(self, subword: Sequence[SymbolType]) -> bool:
        """Check whether the subword is accepted from the current state of the simulator."""
        current_states = self.cur_state  # type: AbstractSet[StateType]
        for symbol in subword:
            current_states = reduce(
                set.union,  # type: ignore
                [self.automaton.get_successors(s, symbol) for s in current_states],
                set(),
            )

        return any(state in self.automaton.accepting_states for state in current_states)
