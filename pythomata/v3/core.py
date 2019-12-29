# -*- coding: utf-8 -*-
"""The core module."""

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Set

StateType = TypeVar('StateType')
SymbolType = TypeVar('SymbolType')
TransitionType = TypeVar('TransitionType')
# StateProperty = TypeVar('StateProperty')
# TransitionProperty = TypeVar('TransitionProperty')


class Alphabet(Generic[SymbolType], ABC):
    """Abstract class to represent the alphabet."""

    @abstractmethod
    def get_symbol(self, index: int) -> SymbolType:
        """
        Get the symbol of the alphabet, given the index.

        :param index: the index.
        :return: the corresponding symbol.
        :raises ValueError: if there is not any symbol for that index.
        """

    @abstractmethod
    def get_symbol_index(self, symbol: SymbolType) -> int:
        """
        Get the index of a symbol of the alphabet.

        :param symbol: the symbol.
        :return: its index.
        :raises ValueError: if the symbol does not belong to the alphabet.
        """

    @property
    @abstractmethod
    def size(self) -> int:
        """
        Get the size of the alphabet.

        :return: the size of the alphabet.
        """

    def contains(self, symbol: SymbolType) -> bool:
        """
        Check if a symbol is part of the alphabet.

        :param symbol: the symbol.
        :return: True if the symbol if part of the alphabet, False otherwise.
        """
        try:
            index = self.get_symbol_index(symbol)
            if index < 0 or index >= self.size:
                return False
            return symbol == self.get_symbol(index)
        except ValueError:
            return False

    @abstractmethod
    def __iter__(self):
        """Iterate over the number of symbols."""


class FiniteAutomaton(Generic[StateType, SymbolType, TransitionType], ABC):
    """This is an interface for any finite state automaton (DFAs, NFAs...)."""

    @property
    @abstractmethod
    def states(self) -> Set[StateType]:
        """
        Get the set of states.

        :return: the set of states of the automaton.
        """

    @property
    @abstractmethod
    def initial_states(self) -> Set[StateType]:
        """Get the set of initial states."""

    @property
    @abstractmethod
    def final_states(self) -> Set[StateType]:
        """Get the set of final states."""

    @abstractmethod
    def get_transitions(self, state: StateType, symbol: SymbolType) -> Set[TransitionType]:
        """
        Get the transitions that can be triggered by the given input symbol.

        :param state: the source state.
        :param symbol: the input symbol.
        :return: the transitions triggered by the given input.
        """

    @abstractmethod
    def get_transition_successor(self, transition: TransitionType) -> StateType:
        """
        Get the successor state of a given transition.

        :param transition: the transition.
        :return: the successor state.
        """

    def get_successors(self, state: StateType, symbol: SymbolType) -> Set[StateType]:
        """
        Get the successors of the state in input when reading a symbol.

        :param state: the state from which to compute the successors.
        :param symbol: the symbol of the transition.
        :return: the set of successor states.
        :raises ValueError: if the state does not belong to the automaton.
        """
        result = set()  # type: Set[StateType]
        transitions = self.get_transitions(state, symbol)
        if len(transitions) == 0:
            return result

        for transition in transitions:
            result.add(self.get_transition_successor(transition))

        return result

    @property
    def size(self) -> int:
        """
        Get the size of the automaton.

        :return: the number of states of the automaton.
        """
        return len(self.states)

    def is_accepting(self, state: StateType) -> bool:
        """
        Check whether a state is accepting.

        :param state: the state of the automaton.
        :return: True if the state is accepting, false otherwise.
        :raises ValueError: if the state does not belong to the automaton.
        """
        return state in self.final_states

    def accepts(self, word: List[SymbolType]) -> bool:
        """
        Check whether the automaton accepts the word.

        :param word: the list of symbols.
        :return: True if the automaton accepts the word, False otherwise.
        """
        current_states = self.initial_states
        for symbol in word:
            next_current_states = set()
            for state in current_states:
                next_current_states.update(self.get_successors(state, symbol))
            current_states = next_current_states

        return any(self.is_accepting(state) for state in current_states)

    #
    # @abstractmethod
    # def add_state(self, state_property: Optional[StateProperty] = None) -> StateType:
    #     """
    #     Create and return a new state.
    #
    #     :param state_property: the state property of a new state.
    #     :return: the new state.
    #     """
    #
    # @abstractmethod
    # def set_initial_state(self, state: StateType, initial: bool) -> None:
    #     """
    #     Set a state as initial state or not.
    #
    #     :param state: a state of the automaton.
    #     :param initial: whether it should be set as initial or not.
    #     :return: None.
    #     :raises ValueError: if the state does not belong to the automaton.
    #     """
    #
    # @abstractmethod
    # def set_state_property(self, state: StateType, state_property: StateProperty) -> None:
    #     """
    #     Set the state property.
    #
    #     :param state: the state.
    #     :param state_property: the state property.
    #     :return: None.
    #     :raises ValueError: if the state does not belong to the automaton.
    #     """
    #
    # @abstractmethod
    # def create_transition(self, successor: StateType, transition_property: TransitionProperty) ->
    # TransitionType:
    #     """
    #     Create a new transition.
    #
    #     :param successor: the successor of the new transition.
    #     :param transition_property: the transition property.
    #     :return: the new transition.
    #     """
    #
    #
    # @abstractmethod
    # def get_successor(self, transition: TransitionType) -> StateType:
    #     """
    #     Get the successor state of a given transition.
    #
    #     :param transition: a transition of the automaton.
    #     :return: the successor state of the given transition.
    #     :raises ValueError: if the transition does not belong to the automaton.
    #     """
    #
    # @abstractmethod
    # def get_transitions(self, state: StateType, symbol: SymbolType) -> Set[TransitionType]:
    #     """
    #     Get the transitions that can be triggered by the given input symbol from the given state.
    #
    #     param state: a state of the automaton.
    #     :param symbol: a symbol of the alphabet.
    #     :return: the set of transitions.
    #     """
    #
    # @abstractmethod
    # def get_state_property(self, state: StateType) -> StateProperty:
    #     """
    #     Get the state property of a state.
    #
    #     :param state: a state of the automaton.
    #     :return: its state property.
    #     """
    #
    # @abstractmethod
    # def get_transition_property(self, transition: TransitionType) -> TransitionProperty:
    #     """
    #     Get the transition property of a transition.
    #
    #     :param transition: a transition of the automaton.
    #     :return: its transition property.
    #     """


class DFA(FiniteAutomaton[StateType, SymbolType, TransitionType], ABC):
    """An interface for a deterministic finite state automaton."""

    @property
    @abstractmethod
    def initial_state(self) -> StateType:
        """Get the (unique) initial state."""

    @abstractmethod
    def get_transition(self, state: StateType, symbol: SymbolType) -> TransitionType:
        """Get the (unique) transition that can be triggered by the given input symbol."""

    def get_transitions(self, state: StateType, symbol: SymbolType) -> Set[TransitionType]:
        """
        Get the transitions that can be triggered by the given input symbol.

        :param state: the source state.
        :param symbol: the input symbol.
        :return: the transitions triggered by the given input.
        """
        return {self.get_transition(state, symbol)}

    @property
    def initial_states(self) -> Set[StateType]:
        """Get the set of initial states."""
        return {self.initial_state}
