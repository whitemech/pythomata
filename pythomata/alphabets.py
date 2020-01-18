# -*- coding: utf-8 -*-
"""This module provides many popular alphabets."""
import itertools
from typing import List, Tuple, Iterable, Iterator, Generic, Union, Collection, Set

from pythomata.core import Alphabet, SymbolType

AlphabetLike = Union[Alphabet[SymbolType], Collection[SymbolType], Set[SymbolType]]

IndexNotFound = ValueError("No symbol for that index.")
SymbolNotFound = ValueError("No symbol for that index.")


class ArrayAlphabet(Alphabet[SymbolType]):
    """An alphabet implemented with an array."""

    def __init__(self, symbols: List[SymbolType]):
        """Initialize the array alphabet."""
        self.symbols = tuple(symbols)  # type: Tuple[SymbolType, ...]

    def get_symbol(self, index: int) -> SymbolType:
        """
        Get the symbol of the alphabet, given the index.

        :param index: the index.
        :return: the corresponding symbol.
        :raises ValueError: if there is not any symbol for that index.
        """
        try:
            return self.symbols[index]
        except IndexError:
            raise IndexNotFound

    def get_symbol_index(self, symbol: SymbolType) -> int:
        """
        Get the index of a symbol of the alphabet.

        :param symbol: the symbol.
        :return: its index.
        :raises ValueError: if the symbol does not belong to the alphabet.
        """
        index = self.__get_symbol_index(symbol)

        if index == -1:
            raise SymbolNotFound

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

    def __iter__(self) -> Iterable[SymbolType]:
        """Iterate over the alphabet."""
        return iter(self.symbols)


class MapAlphabet(Alphabet[SymbolType]):
    """An alphabet implemented with a mapping."""

    def __init__(self, symbols: Iterable[SymbolType]):
        """Initialize the array alphabet."""
        self.symbols = tuple(symbols)  # type: Tuple[SymbolType, ...]
        self.symbol_to_index = dict(map(reversed, enumerate(symbols)))  # type: ignore

    def get_symbol(self, index: int) -> SymbolType:
        """
        Get the symbol of the alphabet, given the index.

        :param index: the index.
        :return: the corresponding symbol.
        :raises ValueError: if there is not any symbol for that index.
        """
        try:
            return self.symbols[index]
        except KeyError:
            raise IndexNotFound

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
        """Iterate over the alphabet."""
        return iter(self.symbols)


class RangeIntAlphabet(Alphabet[int]):
    """
    Use ranges to represent a collection of symbols.

    This alphabet does not store the list of elements explicitly,
    but it only stores the start and the end element of the range.
    """

    def __init__(self, stop: int, start: int = 0, step: int = 1):
        """
        Initialize the range (start included, end NOT included).

        :param start: the start of the range (included)
        :param stop: the end of the range (excluded)
        :param step: the step for the range.
        """
        assert start < stop, "Start must be lower than stop."
        self.r = range(start, stop, step)

    def get_symbol(self, index: int) -> int:
        """Get the symbol associated to the index."""
        try:
            return self.r[index]
        except IndexError:
            raise IndexNotFound

    def get_symbol_index(self, symbol: int) -> int:
        """Get the index, given the symbol."""
        return self.r.index(symbol)

    @property
    def size(self) -> int:
        """Get the size of the alphabet."""
        return len(self.r)

    def __iter__(self):
        """Iterate over the alphabet."""
        return self.r


def from_array(symbols: Iterable[SymbolType]) -> Alphabet:
    """Get an alphabet from arrays."""
    return ArrayAlphabet(list(symbols))


class VectorizedAlphabet(Generic[SymbolType], Alphabet[Tuple[SymbolType, ...]]):
    """
    Vectorized version of an alphabet.

    The result of this operation is a new alphabet whose symbols
    are vectors of symbols of the original alphabet.
    """

    def __init__(self, alphabet: Alphabet[SymbolType], n: int):
        """
        Initialize the vectorized alphabet.

        :param alphabet: the alphabet.
        :param n: the number of desired dimensions.
        :return: the vectorized alphabet.
        """
        self._alphabet = alphabet
        self.n = n

    def get_symbol(self, index: int) -> Tuple[SymbolType, ...]:
        """Get the symbol from an index."""
        symbol_vector = []
        reminder_index = index
        i = self.n - 1
        while i >= 0:
            new_index = reminder_index // (self._alphabet.size ** i)
            new_symbol = self._alphabet.get_symbol(new_index)
            symbol_vector.append(new_symbol)
            reminder_index %= self._alphabet.size ** i
            i -= 1
        return tuple(symbol_vector)

    def get_symbol_index(self, vector: Tuple[SymbolType, ...]) -> int:
        """Get the index of a symbol."""
        if len(vector) != self.n:
            raise SymbolNotFound
        index_of_vector = 0
        for _position, symbol in enumerate(vector):
            index = self._alphabet.get_symbol_index(symbol)
            index_of_vector = index_of_vector * self._alphabet.size
            index_of_vector += index
        return index_of_vector

    @property
    def size(self) -> int:
        """Get the size of the alphabet."""
        return self._alphabet.size ** self.n

    def __iter__(self) -> Iterator[Tuple[SymbolType, ...]]:
        """Iterate over the alphabet."""
        index_vector_iterable = itertools.product(range(self.size), repeat=self.n)
        return map(
            lambda x: tuple([self._alphabet.get_symbol(idx) for idx in x]),
            index_vector_iterable,
        )


class SymbolicAlphabet(Alphabet[str]):
    """
    The alphabet used by a Symbolic automaton.

    >>> alphabet = SymbolicAlphabet(5)
    >>> alphabet.get_symbol(0)
    '00000'

    >>> alphabet.get_symbol(1)
    '00001'

    >>> alphabet.get_symbol_index("00010")
    2

    >>> alphabet.size  # 2 ** 5
    32

    >>> alphabet.get_symbol_index("0000")  # length is not correct
    Traceback (most recent call last):
    ...
    ValueError: No symbol for that index.

    >>> alphabet.get_symbol_index("00002")  # forbidden symbol - only one of 0, 1 or X
    Traceback (most recent call last):
    ...
    ValueError: No symbol for that index.
    """

    def __init__(self, nb_propositions: int):
        """
        Initialize a Symbolic Alphabet.

        :param nb_propositions: the number of propositions.
        """
        self.nb_propositions = nb_propositions
        self._inner_alphabet = VectorizedAlphabet(
            ArrayAlphabet[str](["0", "1"]), nb_propositions
        )

    def get_symbol(self, index: int) -> str:
        """Get a symbol given its index."""
        return "".join(self._inner_alphabet.get_symbol(index))

    def get_symbol_index(self, symbol: str) -> int:
        """Get the index of a symbol."""
        return self._inner_alphabet.get_symbol_index(tuple(symbol))

    @property
    def size(self) -> int:
        """Get the size of the alphabet."""
        return self._inner_alphabet.size

    def __iter__(self):
        """Iterate over the alphabet."""
        return iter(self._inner_alphabet)
