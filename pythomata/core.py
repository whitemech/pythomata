"""The core module."""

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, FrozenSet

StateType = TypeVar('StateType')
SymbolType = TypeVar('SymbolType')


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

    @abstractmethod
    @property
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


class FiniteAutomaton(Generic[StateType, SymbolType], ABC):
    """This is an interface for any finite state automaton (DFAs, NFAs...)."""

    @abstractmethod
    def accepts(self, word: List[SymbolType]) -> bool:
        """
        Check whether the automaton accepts the word.

        :param word: the list of symbols.
        :return: True if the automaton accepts the word, False otherwise.
        """

    @abstractmethod
    def empty(self) -> bool:
        """
        Check whether the automaton corresponds to the empty language.

        :return: True if the automaton accepts the empty language, False otherwise.
        """

    @abstractmethod
    @property
    def states(self) -> FrozenSet[StateType]:
        """
        Get the set of states.

        :return: the set of states of the automaton.
        """
