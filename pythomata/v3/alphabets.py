"""This module provides many popular alphabets."""
from typing import List, Dict, Tuple, Collection, Iterable

from pythomata.v3.core import SymbolType, Alphabet


class ArrayAlphabet(Alphabet[SymbolType]):
    """An alphabet implemented with an array."""

    def __init__(self, symbols: List[SymbolType]):
        """Initialize the array alphabet."""
        self.symbols = tuple(symbols)  # type: Tuple[SymbolType]

    def get_symbol(self, index: int) -> SymbolType:
        """
        Get the symbol of the alphabet, given the index.

        :param index: the index.
        :return: the corresponding symbol.
        :raises ValueError: if there is not any symbol for that index.
        """
        return self.symbols[index]

    def get_symbol_index(self, symbol: SymbolType) -> int:
        """
        Get the index of a symbol of the alphabet.

        :param symbol: the symbol.
        :return: its index.
        :raises ValueError: if the symbol does not belong to the alphabet.
        """
        index = self.__get_symbol_index(symbol)

        if index == -1:
            raise ValueError("Symbol not found.")

        return index

    def __get_symbol_index(self, symbol: SymbolType) -> int:
        """
        Iterate over the list of symbols and find the index.

        :param symbol: the symbol whose index is requested.
        :return: its index, or -1 if not found.
        """
        for idx, sym in enumerate(self.symbols):
            if sym == symbol:
                return idx
        return -1

    @property
    def size(self) -> int:
        """
        Get the size of the alphabet.

        :return: the size of the alphabet.
        """
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)


class MapAlphabet(Alphabet[SymbolType]):
    """An alphabet implemented with a mapping."""

    def __init__(self, symbols: Iterable[SymbolType]):
        """Initialize the array alphabet."""
        self.symbols = tuple(symbols)  # type: Tuple[SymbolType]
        self.symbol_to_index = dict(map(reversed, enumerate(symbols)))  # type: Dict[int, SymbolType]

    def get_symbol(self, index: int) -> SymbolType:
        """
        Get the symbol of the alphabet, given the index.

        :param index: the index.
        :return: the corresponding symbol.
        :raises ValueError: if there is not any symbol for that index.
        """
        return self.symbols[index]

    def get_symbol_index(self, symbol: SymbolType) -> int:
        """
        Get the index of a symbol of the alphabet.

        :param symbol: the symbol.
        :return: its index.
        :raises ValueError: if the symbol does not belong to the alphabet.
        """
        return self.symbol_to_index[symbol]

    @property
    def size(self) -> int:
        """
        Get the size of the alphabet.

        :return: the size of the alphabet.
        """
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)


def from_array(symbols: Collection[SymbolType]):
    """Get an alphabet from arrays."""
    return ArrayAlphabet(symbols)

