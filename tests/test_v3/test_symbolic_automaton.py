# -*- coding: utf-8 -*-
import itertools

import pytest
from sympy import Symbol
from sympy.logic.boolalg import BooleanTrue

from pythomata.v3.dfas.symbolic import SymbolicAutomaton


class TestSymbolicAutomatonEmptyLanguage:
    """Test the symbolic automaton of the empty language."""

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


class TestSymbolicAutomatonEmptyStringLanguage:
    """Test the symbolic automaton recognizes the language with only the empty string."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()
        cls.automaton.set_final_state(0, True)

    def test_accepts(self):
        """Test the accepts work as expected."""
        assert self.automaton.accepts([])
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
        assert self.automaton.final_states == {0}

    def test_size(self):
        """Test size."""
        assert self.automaton.size == 1

    def test_get_successors(self):
        """Test get successors."""
        assert self.automaton.get_successors(0, {}) == set()

    def test_is_accepting(self):
        """Test is_accepting."""
        assert self.automaton.is_accepting(0)


class TestSymbolicAutomatonSingletonLanguage:
    """
    Test the symbolic automaton recognizes a singleton language.

    In this test, the automaton can only accepts the word 'a'.
    """

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()
        new_state = cls.automaton.create_state()
        assert new_state == 1
        cls.automaton.set_final_state(new_state, True)

        a = Symbol("a")
        cls.automaton.add_transition(0, a, new_state)

    def test_accepts(self):
        """Test the accepts work as expected."""
        assert not self.automaton.accepts([])

        assert not self.automaton.accepts([{}])
        assert self.automaton.accepts([{"a": True}])
        assert self.automaton.accepts([{"a": True, "b": False}])

        assert not self.automaton.accepts([{}, {}])
        assert not self.automaton.accepts([{"a": True}, {"b": False}])

    def test_states(self):
        """Test the set of states is correct."""
        assert self.automaton.states == {0, 1}

    def test_initial_states(self):
        """Test initial states."""
        assert self.automaton.initial_states == {0}

    def test_final_states(self):
        """Test initial states."""
        assert self.automaton.final_states == {1}

    def test_size(self):
        """Test size."""
        assert self.automaton.size == 2

    def test_get_successors(self):
        """Test get successors."""
        assert self.automaton.get_successors(0, {}) == set()
        assert self.automaton.get_successors(0, {"a": True}) == {1}
        assert self.automaton.get_successors(1, {}) == set()

    def test_is_accepting(self):
        """Test is_accepting."""
        assert not self.automaton.is_accepting(0)
        assert self.automaton.is_accepting(1)


class TestSymbolicAutomatonUniversalLanguage:
    """Test the symbolic automaton recognizes the universal language."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()
        cls.automaton.set_final_state(0, True)
        cls.automaton.add_transition(0, BooleanTrue(), 0)

    def test_accepts(self):
        """Test the accepts work as expected."""
        assert self.automaton.accepts([])

        assert self.automaton.accepts([{}])
        assert self.automaton.accepts([{"a": True}])
        assert self.automaton.accepts([{"a": True, "b": False}])

        assert self.automaton.accepts([{}, {}])
        assert self.automaton.accepts([{"a": True}, {"b": False}])
        assert self.automaton.accepts([{}] * 200)

    def test_states(self):
        """Test the set of states is correct."""
        assert self.automaton.states == {0}

    def test_initial_states(self):
        """Test initial states."""
        assert self.automaton.initial_states == {0}

    def test_final_states(self):
        """Test initial states."""
        assert self.automaton.final_states == {0}

    def test_size(self):
        """Test size."""
        assert self.automaton.size == 1

    def test_get_successors(self):
        """Test get successors."""
        assert self.automaton.get_successors(0, {}) == {0}
        assert self.automaton.get_successors(0, {"a": True}) == {0}

    def test_is_accepting(self):
        """Test is_accepting."""
        assert self.automaton.is_accepting(0)


class TestDeterminize:
    """Test 'determinize' of a symbolic automaton."""

    @classmethod
    def setup_class(cls):
        """Set the tests up."""
        cls.automaton = SymbolicAutomaton()
        new_state_1 = cls.automaton.create_state()
        new_state_2 = cls.automaton.create_state()
        cls.automaton.set_final_state(new_state_1, True)
        cls.automaton.add_transition(0, "x | y", new_state_1)
        cls.automaton.add_transition(0, "x | z", new_state_2)

        cls.determinized = cls.automaton.determinize()

    def test_get_successors(self):
        """Test get successors of determinized automaton."""
        assert self.automaton.get_successors(0, {"x": True}) == {1, 2}
        # we cannot assert the actual result since the state name is not deterministic.
        assert len(self.determinized.get_successors(0, {"x": True})) == 1

    @pytest.mark.parametrize("trace", [
        [],
        *itertools.product(map(lambda x: dict(zip("xyz", x)), itertools.product([True, False], repeat=3)), repeat=1),
        *itertools.product(map(lambda x: dict(zip("xyz", x)), itertools.product([True, False], repeat=3)), repeat=2)
    ])
    def test_accepts(self, trace):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(trace) == self.determinized.accepts(trace)
