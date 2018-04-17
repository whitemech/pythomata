from typing import Set, Any

from pythomata.base.Symbol import Symbol


class Alphabet(object):
    def __init__(self, symbols: Set[Symbol]):
        self.symbols = symbols

    @staticmethod
    def fromObjects(symbols:Set[Any]):
        return Alphabet(set(Symbol(s) for s in symbols))

    def __eq__(self, other):
        if type(self)==type(other):
            return self.symbols == other.symbols
        else:
            return False
