# -*- coding: utf-8 -*-
import itertools

import pytest
from sympy import Symbol
from sympy.logic.boolalg import BooleanTrue

from pythomata import SymbolicAutomaton


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
        assert self.automaton.states == set()

    def test_initial_states(self):
        """Test initial states."""
        assert self.automaton.initial_states == set()

    def test_final_states(self):
        """Test initial states."""
        assert self.automaton.final_states == set()

    def test_size(self):
        """Test size."""
        assert self.automaton.size == 0


class TestSymbolicAutomatonEmptyStringLanguage:
    """Test the symbolic automaton recognizes the language with only the empty string."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()
        cls.automaton.create_state()
        cls.automaton.set_initial_state(0, True)
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
        state_0 = cls.automaton.create_state()
        state_1 = cls.automaton.create_state()
        cls.automaton.set_initial_state(state_0, True)
        cls.automaton.set_final_state(state_1, True)

        a = Symbol("a")
        cls.automaton.add_transition(state_0, a, state_1)

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
        state_0 = cls.automaton.create_state()
        cls.automaton.set_initial_state(state_0, True)
        cls.automaton.set_final_state(state_0, True)
        cls.automaton.add_transition(state_0, BooleanTrue(), state_0)

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
        state_0 = cls.automaton.create_state()
        state_1 = cls.automaton.create_state()
        state_2 = cls.automaton.create_state()
        cls.automaton.set_initial_state(state_0, True)
        cls.automaton.set_final_state(state_1, True)
        cls.automaton.add_transition(state_0, "x | y", state_1)
        cls.automaton.add_transition(state_0, "x | z", state_2)

        cls.determinized = cls.automaton.determinize()

    def test_size(self):
        """Test the size of the determinized automaton."""
        return self.determinized.size == 4

    def test_get_successors(self):
        """Test get successors of determinized automaton."""
        # we cannot assert the actual result since the state name is not deterministic.
        assert len(self.determinized.initial_states) == 1
        initial_state = next(iter(self.determinized.initial_states))
        assert len(self.automaton.get_successors(0, {"x": True})) == 2
        assert len(self.determinized.get_successors(initial_state, {"x": True})) == 1

    @pytest.mark.parametrize("trace", [
        [],
        *itertools.product(map(lambda x: dict(zip("xyz", x)), itertools.product([True, False], repeat=3)), repeat=1),
        *itertools.product(map(lambda x: dict(zip("xyz", x)), itertools.product([True, False], repeat=3)), repeat=2)
    ])
    def test_accepts(self, trace):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(trace) == self.determinized.accepts(trace)


class TestComplete:
    """Test the 'complete' method of a symbolic automaton."""

    @classmethod
    def setup_class(cls):
        """Set the tests up."""
        cls.automaton = SymbolicAutomaton()
        state_0 = cls.automaton.create_state()
        state_1 = cls.automaton.create_state()
        state_2 = cls.automaton.create_state()
        cls.automaton.set_initial_state(state_0, True)
        cls.automaton.set_final_state(state_1, True)
        cls.automaton.add_transition(state_0, "x | y", state_1)
        cls.automaton.add_transition(state_0, "x | z", state_2)

        cls.completed = cls.automaton.complete()

    def test_size(self):
        """Test the size of the determinized automaton."""
        return self.completed.size == 4

    def test_initial_states(self):
        """Test initial states."""
        assert self.completed.initial_states == {0}

    def test_get_successors(self):
        """Test get successors of completed automaton."""
        assert self.completed.get_successors(0, {"x": True}) == {1, 2}
        assert self.completed.get_successors(0, {"x": False}) == {3}

        assert self.completed.get_successors(1, {"x": True}) == {3}
        assert self.completed.get_successors(1, {"x": False}) == {3}

        assert self.completed.get_successors(2, {"x": True}) == {3}
        assert self.completed.get_successors(2, {"x": False}) == {3}

        assert self.completed.get_successors(3, {"x": True}) == {3}
        assert self.completed.get_successors(3, {"x": False}) == {3}

    @pytest.mark.parametrize("trace", [
        [],
        *itertools.product(map(lambda x: dict(zip("xyz", x)), itertools.product([True, False], repeat=3)), repeat=1),
        *itertools.product(map(lambda x: dict(zip("xyz", x)), itertools.product([True, False], repeat=3)), repeat=2)
    ])
    def test_accepts(self, trace):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(trace) == self.completed.accepts(trace)


def test_to_graphviz():
    """Test 'to_graphviz' method."""

    automaton = SymbolicAutomaton()
    state_0 = automaton.create_state()
    state_1 = automaton.create_state()
    state_2 = automaton.create_state()
    automaton.set_initial_state(state_0, True)
    automaton.set_final_state(state_1, True)
    automaton.add_transition(state_0, "x | y", state_1)
    automaton.add_transition(state_0, "x | z", state_2)

    automaton.to_graphviz(title="test dfa (initial state final)")
