# -*- coding: utf-8 -*-
import pytest

from pythomata.v3.alphabets import MapAlphabet
from pythomata.v3.dfas.symbolic import SymbolicAutomaton
from pythomata.v3.dfas.simple import SimpleDFA


class TestSymbolicAutomatonEmptyLanguage:
    """Basic tests for the symbolic automaton implementation."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()

    def test_accepts(self):
        """Test the accepts work as expected."""
        assert not self.automaton.accepts([])
        assert not self.automaton.accepts([{}])
        assert not self.automaton.accepts([{"a": False}])

    def test_states(self):
        """Test the set of states is correct."""
        assert self.automaton.states == {0}

    def test_initial_states(self):
        """Test initial states."""
        assert self.automaton.initial_states == {0}

    def test_final_states(self):
        """Test initial states."""
        assert self.automaton.final_states == set()

    def test_size(self):
        """Test size."""
        assert self.automaton.size == 1

    def test_get_successors(self):
        """Test get successors."""
        assert self.automaton.get_successors(0, {}) == set()

    def test_successor_with_non_alphabet_symbol(self):
        """Test the 'get_successors' with a non-alphabet symbol."""
        with pytest.raises(ValueError, match="Symbol wrong_symbol is not valid."):
            self.automaton.get_successors(0, 'wrong_symbol')

    def test_is_accepting(self):
        """Test is_accepting."""
        assert not self.automaton.is_accepting(0)
