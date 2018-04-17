# -*- coding: utf-8 -*-
from typing import Hashable


class Symbol(object):
    """A class to represent a symbol"""
    def __init__(self, name:Hashable):
        self.name = name

    def __str__(self):
        return str(self.name)

    def _members(self):
        return (self.name)

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())

    def __repr__(self):
        return str(self._members())

    def __lt__(self, other):
        return self.name.__lt__(other.name)
