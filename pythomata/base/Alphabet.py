from typing import Set

from pythomata.base.Symbol import Symbol


class Alphabet(object):
    def __init__(self, symbols: Set[Symbol]):
        self.symbols = symbols

    @staticmethod
    def fromStrings(symbol_strings:Set[str]):
        return Alphabet(set(Symbol(s) for s in symbol_strings))

    def __eq__(self, other):
        if type(self)==type(other):
            return self.symbols == other.symbols
        else:
            return False
