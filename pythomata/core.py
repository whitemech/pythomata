# -*- coding: utf-8 -*-
"""The core module."""
from abc import ABC, abstractmethod
from functools import reduce
from typing import TypeVar, Generic, AbstractSet, Optional, Tuple, Dict, Any, Sequence

import graphviz

StateType = TypeVar("StateType")
SymbolType = TypeVar("SymbolType")
GuardType = TypeVar("GuardType")
TransitionType = Tuple[StateType, GuardType, StateType]


class Alphabet(Generic[SymbolType], ABC):
    """Abstract class to represent a finite alphabet."""

    @abstractmethod
    def get_symbol(self, index: int) -> SymbolType:
        """
        Get the symbol of the alphabet, given the index.

        :param index: the index.
        :return: the corresponding symbol.
        :raise ValueError: if there is not any symbol for that index.
        """

    @abstractmethod
    def get_symbol_index(self, symbol: SymbolType) -> int:
        """
        Get the index of a symbol of the alphabet.

        :param symbol: the symbol.
        :return: its index.
        :raise ValueError: if the symbol does not belong to the alphabet.
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

    def __len__(self):
        """Return the size of the alphabet."""
        return self.size

    def __eq__(self, other) -> bool:
        """Check that two alphabet are equal."""
        return isinstance(other, Alphabet) and set(self) == set(other)


class FiniteAutomaton(Generic[StateType, SymbolType, GuardType], ABC):
    """
    This is an interface for any finite state automaton (DFAs, NFAs...).

    The implementer of this interface must decide:
    - `StateType`, namely the type of state to use (e.g. integers, strings, ...);
    - `SymbolType`, namely the type of symbol that the automaton can read;
    - `GuardType`, namely the type of guard (e.g. symbol, propositional formulas, ...).

    A transition is a triple `(source, guard, destination)`, where
    `source` and `destination` are instances of the `StateType` class,
    whereas `guard` is an instance of `GuardType`.

    By convention, the automaton must have at least one state, and only one
    of them is an initial state.
    """

    def __init__(self):
        """Initialize the finite automaton."""
        self._state_attributes = {}  # type: Dict[StateType, Dict[str, Any]]
        self._transition_attributes = {}  # type: Dict[TransitionType, Dict[str, Any]]

    @property
    @abstractmethod
    def states(self) -> AbstractSet[StateType]:
        """
        Get the set of states.

        :return: the set of states of the automaton.
        """

    @property
    @abstractmethod
    def initial_state(self) -> StateType:
        """
        Get the initial state.

        :return: the initial state.
        """

    @property
    @abstractmethod
    def accepting_states(self) -> AbstractSet[StateType]:
        """
        Get the set of accepting states.

        :return: the set of accepting states.
        """

    @abstractmethod
    def get_successors(
        self, state: StateType, symbol: SymbolType
    ) -> AbstractSet[StateType]:
        """
        Get the successors of the state in input when reading a symbol.

        :param state: the state from which to compute the successors.
        :param symbol: the symbol of the transition.
        :return: the set of successor states.
        :raise ValueError: if the state does not belong to the automaton, or the symbol is not correct.
        """

    def get_transitions_from(self, state: StateType) -> AbstractSet[TransitionType]:
        """
        Get the outgoing transitions from a state.

        A transition is a triple (source_state, guard, destination_state).

        For some implementations, this method might make no sense. Hence,
        the implementation of this method is optional. However, some
        features that use this method might not work (e.g. the rendering).

        :param state: the source state.
        :return: the set of transitions object associated with that triple.
        :raise ValueError: if the state does not belong to the automaton.
        """
        raise NotImplementedError

    def get_transitions(self) -> AbstractSet[TransitionType]:
        """
        Get all the transitions.

        :return: the set of transitions.
        """
        transitions = set()
        for state in self.states:
            for start_state, guard, end_state in self.get_transitions_from(state):
                transitions.add((start_state, guard, end_state))
        return transitions

    def get_state_attribute(self, state: StateType, attr_name: str) -> Optional[Any]:
        """
        Get a state attribute.

        :param state: the state.
        :param attr_name: the attribute name.
        :return: the attribute value.
        """
        return self._state_attributes.get(state, {}).get(attr_name, None)

    def set_state_attribute(
        self, state: StateType, attr_name: str, attr_value: Any
    ) -> None:
        """
        Set a state attribute.

        :param state: the state.
        :param attr_name: the attribute name.
        :param attr_value: the attribute value.
        :return: the attribute value.
        """
        self._state_attributes.get(state, {})[attr_name] = attr_value

    def get_transition_attribute(
        self, transition: TransitionType, attr_name: str
    ) -> Optional[Any]:
        """
        Get a transition attribute.

        :param transition: the transition.
        :param attr_name: the attribute name.
        :return: the attribute value.
        """
        return self._transition_attributes.get(transition, {}).get(attr_name, None)

    def set_transition_attribute(
        self, transition: TransitionType, attr_name: str, attr_value: Any
    ) -> None:
        """
        Set a transition attribute.

        :param transition: the transition.
        :param attr_name: the attribute name.
        :param attr_value: the attribute value.
        :return: the attribute value.
        """
        self._transition_attributes.get(transition, {})[attr_name] = attr_value

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
        :raise ValueError: if the state does not belong to the automaton.
        """
        if state not in self.states:
            raise ValueError("The state does not belong to the automaton.")
        return state in self.accepting_states

    def accepts(self, word: Sequence[SymbolType]) -> bool:
        """
        Check whether the automaton accepts the word.

        :param word: the list of symbols.
        :return: True if the automaton accepts the word, False otherwise.
        """
        current_states = {self.initial_state}  # type: AbstractSet[StateType]
        for symbol in word:
            current_states = reduce(
                set.union,  # type: ignore
                map(lambda x: self.get_successors(x, symbol), current_states),
                set(),
            )

        return any(self.is_accepting(state) for state in current_states)


class DFA(
    FiniteAutomaton[StateType, SymbolType, GuardType],
    Generic[StateType, SymbolType, GuardType],
    ABC,
):
    """An interface for a deterministic finite state automaton."""

    @abstractmethod
    def get_successor(
        self, state: StateType, symbol: SymbolType
    ) -> Optional[StateType]:
        """
        Get the (unique) successor.

        If not defined, return None.
        """

    def get_successors(
        self, state: StateType, symbol: SymbolType
    ) -> AbstractSet[StateType]:
        """Get the successors."""
        successor = self.get_successor(state, symbol)
        return {successor} if successor is not None else set()


class Rendering(
    FiniteAutomaton[StateType, SymbolType, GuardType],
    Generic[StateType, SymbolType, GuardType],
    ABC,
):
    """The automaton class that implements this interface can use rendering functionalities."""

    def to_graphviz(self) -> graphviz.Digraph:
        """
        Convert to graphviz.Digraph object.

        :return: the graphviz.Digraph object.
        :raise ValueError: if it was not possible to compute the graph.
        """
        graph = graphviz.Digraph(format="svg")
        graph.node("fake", style="invisible")
        for state in self.states:
            if state == self.initial_state:
                if state in self.accepting_states:
                    graph.node(str(state), root="true", shape="doublecircle")
                else:
                    graph.node(str(state), root="true")
            elif state in self.accepting_states:
                graph.node(str(state), shape="doublecircle")
            else:
                graph.node(str(state))

        graph.edge("fake", str(self.initial_state), style="bold")

        for (start, guard, end) in self.get_transitions():
            graph.edge(str(start), str(end), label=str(guard))

        return graph


class MutableAutomaton(
    Generic[StateType, SymbolType, GuardType],
    FiniteAutomaton[StateType, SymbolType, GuardType],
):
    """This interface refines the FiniteAutomaton interface by adding methods to modify the automaton."""

    @abstractmethod
    def create_state(self) -> StateType:
        """
        Create a state.

        :return: the new created state.
        """

    @abstractmethod
    def remove_state(self, state: StateType) -> None:
        """
        Remove a state.

        The implementation should also drop all the transitions
        starting from that state.

        :return: None.
        :raise ValueError: if the state does not exist.
        """

    @abstractmethod
    def add_transition(self, transition: TransitionType) -> None:
        """
        Add a transition, i.e. a tuple (source, guard, destination).

        :param transition: the transition to add.
        :return: None
        :raise ValueError: if the source state does not exist.
        :raise ValueError: if the dest state does not exist.
        """

    @abstractmethod
    def remove_transition(self, transition: TransitionType) -> None:
        """
        Remove a transition.

        :param transition: the transition to remove.
        :return: None
        :raise ValueError: if the transition does not exist.
        """

    @abstractmethod
    def set_accepting_state(self, state: int, is_accepting: bool) -> None:
        """
        Set a state to be accepting.

        :param state: a state of the automaton.
        :param is_accepting: whether the state is an accepting state or not.
        :return: None
        :raise ValueError: if the state does not exist.
        """

    @abstractmethod
    def set_initial_state(self, state: int) -> None:
        """
        Set a state to be initial.

        This method overwrites the previous initial state.

        :param state: a state of the automaton.
        :return: None
        :raise ValueError: if the state does not exist.
        """


# not used yet
class AutomataOperations(Generic[StateType, SymbolType], ABC):
    """An interface for automata operations."""

    @abstractmethod
    def determinize(self) -> DFA[StateType, SymbolType, GuardType]:
        """Make the automaton deterministic."""

    @abstractmethod
    def minimize(self) -> FiniteAutomaton[StateType, SymbolType, GuardType]:
        """Minimize the automaton."""
