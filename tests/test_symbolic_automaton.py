# -*- coding: utf-8 -*-
import sympy
from hypothesis import given
from sympy import Symbol
from sympy.logic.boolalg import BooleanTrue

from pythomata import SymbolicAutomaton
from .strategies import words


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

    @given(words(list("xyz"), min_size=0, max_size=2))
    def test_accepts(self, trace):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(trace) == self.determinized.accepts(trace)


class TestDeterminize2:
    """Test determinize."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        A, B, C = sympy.symbols("A B C")
        aut = SymbolicAutomaton()
        aut.create_state()
        aut.create_state()
        aut.create_state()
        aut.create_state()
        aut.set_initial_state(3, True)
        aut.set_final_state(0, True)
        aut.set_final_state(1, True)

        trfun = {
            3: {0: A | ~B, 2: B & ~A},
            0: {1: BooleanTrue()},
            2: {2: BooleanTrue()},
            1: {1: BooleanTrue()},
        }
        for s in trfun:
            for d, guard in trfun[s].items():
                aut.add_transition(s, guard, d)

        cls.automaton = aut
        cls.determinized = aut.determinize()

    @given(words(list("ABC"), min_size=0, max_size=2))
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

    def test_is_complete(self):
        """Test is complete."""
        assert not self.automaton.is_complete()
        assert self.completed.is_complete()

    @given(words(list("xyz"), min_size=0, max_size=2))
    def test_accepts(self, trace):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(trace) == self.completed.accepts(trace)


class TestMinimize:
    @classmethod
    def setup_class(cls):
        """Set the tests up."""
        cls.automaton = SymbolicAutomaton()
        automaton = cls.automaton
        q0 = automaton.create_state()
        q1 = automaton.create_state()
        q2 = automaton.create_state()
        q3 = automaton.create_state()
        q4 = automaton.create_state()

        automaton.set_initial_state(q0, True)
        automaton.set_final_state(q3, True)
        automaton.set_final_state(q4, True)

        automaton.add_transition(q0, "a", q1)
        automaton.add_transition(q0, "b", q2)
        automaton.add_transition(q1, "c", q3)
        automaton.add_transition(q2, "c", q3)
        automaton.add_transition(q3, "c", q4)
        automaton.add_transition(q4, "c", q4)

        cls.minimized = automaton.minimize()

    def test_states(self):
        # the renaming of the states is non deterministic, so we need to compare every substructure.
        assert self.minimized.size == 4

    @given(words(list("abc"), min_size=0, max_size=5))
    def test_accepts(self, trace):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(trace) == self.minimized.accepts(trace)

    def test_minimized_is_complete(self):
        """Test that every minimized DFA is complete."""
        assert self.minimized.is_complete()


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

    automaton.to_graphviz()
