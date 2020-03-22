# -*- coding: utf-8 -*-
"""Test symbolic automaton."""
from functools import reduce

import pytest
import sympy
from hypothesis import given
from sympy import Symbol
from sympy.logic.boolalg import BooleanTrue

from pythomata import SymbolicAutomaton
from pythomata.impl.symbolic import SymbolicDFA
from pythomata.simulator import AutomatonSimulator
from .strategies import propositional_words


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

    def test_initial_state(self):
        """Test initial state."""
        assert self.automaton.initial_state == 0

    def test_final_states(self):
        """Test initial states."""
        assert self.automaton.accepting_states == set()

    def test_size(self):
        """Test size."""
        assert self.automaton.size == 1


class TestSymbolicAutomatonEmptyStringLanguage:
    """Test the symbolic automaton recognizes the language with only the empty string."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()
        cls.automaton.set_initial_state(0)
        cls.automaton.set_accepting_state(0, True)

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
        assert self.automaton.initial_state == 0

    def test_final_states(self):
        """Test initial states."""
        assert self.automaton.accepting_states == {0}

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
        state_0 = 0
        state_1 = cls.automaton.create_state()
        cls.automaton.set_initial_state(state_0)
        cls.automaton.set_accepting_state(state_1, True)

        a = Symbol("a")
        cls.automaton.add_transition((state_0, a, state_1))

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
        assert self.automaton.initial_state == 0

    def test_final_states(self):
        """Test initial states."""
        assert self.automaton.accepting_states == {1}

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


class TestCreateState:
    """Test 'create_state" method."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()

        assert len(cls.automaton.states) == 1
        assert cls.automaton.states == {0}

        cls.new_state = cls.automaton.create_state()

    def test_new_state_created(self):
        """Test create state works as expected."""
        assert self.automaton.states == {0, 1}


class TestRemoveState:
    """Test 'remove_state" method."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()

        assert len(cls.automaton.states) == 1
        assert cls.automaton.states == {0}

        cls.new_state = cls.automaton.create_state()
        assert cls.automaton.states == {0, 1}

    def test_state_removed(self):
        """Test remove state works as expected."""
        self.automaton.remove_state(self.new_state)
        assert self.automaton.states == {0}


class TestRemoveNonExistingState:
    """Test 'remove_state" with a non-existing state."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()

        assert len(cls.automaton.states) == 1
        assert cls.automaton.states == {0}

    def test_removing_initial_state_raises_exception(self):
        """Test remove state raises ValueError when try to remove initial state."""
        with pytest.raises(ValueError, match="State 42 not found."):
            self.automaton.remove_state(42)


class TestRemoveInitialState:
    """Test 'remove_state" with the initial state in input."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()

        assert len(cls.automaton.states) == 1
        assert cls.automaton.states == {0}

    def test_removing_initial_state_raises_exception(self):
        """Test remove state raises ValueError when try to remove initial state."""
        with pytest.raises(ValueError, match="Cannot remove initial state."):
            self.automaton.remove_state(0)


class TestSymbolicAutomatonUniversalLanguage:
    """Test the symbolic automaton recognizes the universal language."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.automaton = SymbolicAutomaton()
        state_0 = 0
        cls.automaton.set_initial_state(state_0)
        cls.automaton.set_accepting_state(state_0, True)
        cls.automaton.add_transition((state_0, BooleanTrue(), state_0))

    @given(propositional_words(["a", "b"]))
    def test_accepts(self, word):
        """Test the accepts work as expected."""
        assert self.automaton.accepts(word)

    def test_states(self):
        """Test the set of states is correct."""
        assert self.automaton.states == {0}

    def test_initial_states(self):
        """Test initial states."""
        assert self.automaton.initial_state == 0

    def test_final_states(self):
        """Test initial states."""
        assert self.automaton.accepting_states == {0}

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
        state_0 = 0
        state_1 = cls.automaton.create_state()
        state_2 = cls.automaton.create_state()
        cls.automaton.set_initial_state(state_0)
        cls.automaton.set_accepting_state(state_1, True)
        cls.automaton.add_transition((state_0, "x | y", state_1))
        cls.automaton.add_transition((state_0, "x | z", state_2))

        cls.determinized = cls.automaton.determinize()

    def test_size(self):
        """Test the size of the determinized automaton."""
        return self.determinized.size == 4

    def test_get_successors(self):
        """Test get successors of determinized automaton."""
        # we cannot assert the actual result since the state name is not deterministic.
        initial_state = self.automaton.initial_state
        assert len(self.automaton.get_successors(0, {"x": True})) == 2
        assert len(self.determinized.get_successors(initial_state, {"x": True})) == 1

    @given(propositional_words(list("xyz"), min_size=0, max_size=2))
    def test_accepts(self, word):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(word) == self.determinized.accepts(word)


class TestDeterminizeWhenInitialStateIsAccepting:
    """Test determinize when the initial state is accepting."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        A, B, C = sympy.symbols("A B C")
        aut = SymbolicAutomaton()
        aut.create_state()
        aut.create_state()
        aut.create_state()
        aut.set_initial_state(3)
        aut.set_accepting_state(0, True)
        aut.set_accepting_state(1, True)
        aut.set_accepting_state(3, True)

        trfun = {
            3: {0: A | ~B, 2: B & ~A},
            0: {1: BooleanTrue()},
            2: {2: BooleanTrue()},
            1: {1: BooleanTrue()},
        }
        for s in trfun:
            for d, guard in trfun[s].items():
                aut.add_transition((s, guard, d))

        cls.automaton = aut
        cls.determinized = aut.determinize()

    @given(propositional_words(list("ABC"), min_size=0, max_size=2))
    def test_accepts(self, word):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(word) == self.determinized.accepts(word)


class TestComplete:
    """Test the 'complete' method of a symbolic automaton."""

    @classmethod
    def setup_class(cls):
        """Set the tests up."""
        cls.automaton = SymbolicAutomaton()
        state_0 = 0
        state_1 = cls.automaton.create_state()
        state_2 = cls.automaton.create_state()
        cls.automaton.set_initial_state(state_0)
        cls.automaton.set_accepting_state(state_1, True)
        cls.automaton.add_transition((state_0, "x | y", state_1))
        cls.automaton.add_transition((state_0, "x | z", state_2))

        cls.completed = cls.automaton.complete()

    def test_size(self):
        """Test the size of the determinized automaton."""
        return self.completed.size == 4

    def test_initial_states(self):
        """Test initial states."""
        assert self.completed.initial_state == 0

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

    @given(propositional_words(list("xyz"), min_size=0, max_size=2))
    def test_accepts(self, word):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(word) == self.completed.accepts(word)


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

        automaton.set_initial_state(q0)
        automaton.set_accepting_state(q3, True)
        automaton.set_accepting_state(q4, True)

        automaton.add_transition((q0, "a", q1))
        automaton.add_transition((q0, "b", q2))
        automaton.add_transition((q1, "c", q3))
        automaton.add_transition((q2, "c", q3))
        automaton.add_transition((q3, "c", q4))
        automaton.add_transition((q4, "c", q4))

        cls.minimized = automaton.minimize()

    def test_states(self):
        # the renaming of the states is non deterministic, so we need to compare every substructure.
        assert self.minimized.size == 4

    @given(propositional_words(list("abc"), min_size=0, max_size=5))
    def test_accepts(self, word):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(word) == self.minimized.accepts(word)

    def test_minimized_is_complete(self):
        """Test that every minimized DFA is complete."""
        assert self.minimized.is_complete()


class TestMinimizeWhenNoAcceptingState:
    @classmethod
    def setup_class(cls):
        """Set the tests up."""
        cls.automaton = SymbolicDFA()
        automaton = cls.automaton
        q0 = automaton.create_state()
        q1 = automaton.create_state()
        q2 = automaton.create_state()
        q3 = automaton.create_state()
        q4 = automaton.create_state()

        automaton.set_initial_state(q0)
        automaton.add_transition((q0, "a", q1))
        automaton.add_transition((q0, "b", q2))
        automaton.add_transition((q1, "c", q3))
        automaton.add_transition((q2, "c", q3))
        automaton.add_transition((q3, "c", q4))
        automaton.add_transition((q4, "c", q4))

        cls.minimized = automaton.minimize()

    def test_states(self):
        # the renaming of the states is non deterministic, so we need to compare every substructure.
        assert self.minimized.size == 1

    @given(propositional_words(list("abc"), min_size=0, max_size=5))
    def test_accepts(self, word):
        """Test equivalence of acceptance between the two automata."""
        assert self.automaton.accepts(word) == self.minimized.accepts(word)

    def test_minimized_is_complete(self):
        """Test that every minimized DFA is complete."""
        assert self.minimized.is_complete()


def test_to_graphviz():
    """Test 'to_graphviz' method."""

    automaton = SymbolicAutomaton()
    state_0 = automaton.create_state()
    state_1 = automaton.create_state()
    state_2 = automaton.create_state()
    automaton.set_initial_state(state_0)
    automaton.set_accepting_state(state_1, True)
    automaton.add_transition((state_0, "x | y", state_1))
    automaton.add_transition((state_0, "x | z", state_2))

    automaton.to_graphviz()


class TestSimulator:
    """Test the simulator with a SimpleDFA"""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.dfa = SymbolicAutomaton()
        automaton = cls.dfa
        q0 = automaton.create_state()
        q1 = automaton.create_state()
        q2 = automaton.create_state()

        automaton.set_initial_state(q0)
        automaton.set_accepting_state(q2, True)

        automaton.add_transition((q0, "a", q0))
        automaton.add_transition((q0, "b", q1))
        automaton.add_transition((q0, "c", q2))

        automaton.add_transition((q1, "a", q0))
        automaton.add_transition((q1, "b", q1))
        automaton.add_transition((q1, "c", q2))

        automaton.add_transition((q2, "a", q0))
        automaton.add_transition((q2, "b", q1))
        automaton.add_transition((q2, "c", q2))

        # dummy state and transitions to make it non-deterministic
        q3 = automaton.create_state()
        automaton.add_transition((q0, "a", q3))
        automaton.add_transition((q1, "b", q3))
        automaton.add_transition((q2, "c", q3))
        automaton.add_transition((q3, "a", q0))
        automaton.add_transition((q3, "b", q1))
        automaton.add_transition((q3, "c", q2))

    def test_initialization(self):
        """Test the initialization of a simulator."""
        simulator = AutomatonSimulator(self.dfa)

        assert simulator.automaton == self.dfa
        assert simulator.cur_state == {self.dfa.initial_state}
        assert not simulator.is_started

    @given(propositional_words(list("abcd"), min_size=0, max_size=5))
    def test_step(self, word):
        """Test the behaviour of the method 'step'."""
        simulator = AutomatonSimulator(self.dfa)

        for symbol in word:
            previous_states = simulator.cur_state
            current_states = simulator.step(symbol)
            expected_current_states = reduce(
                set.union,
                [self.dfa.get_successors(s, symbol) for s in previous_states],
                set(),
            )
            assert simulator.cur_state == current_states == expected_current_states

    def test_is_true(self):
        """Test the behaviour of the method 'is_true'."""
        simulator = AutomatonSimulator(self.dfa)

        assert not simulator.is_true()
        simulator.step({"a": True})
        assert not simulator.is_true()
        simulator.step({"b": True})
        assert not simulator.is_true()
        simulator.step({"c": True})
        assert simulator.is_true()

    def test_is_failed(self):
        """Test the behaviour of the method 'is_failed'."""
        simulator = AutomatonSimulator(self.dfa)

        assert not simulator.is_failed()
        simulator.step({"a": True})
        assert not simulator.is_failed()
        simulator.step({"b": True})
        assert not simulator.is_failed()
        simulator.step({"c": True})
        assert not simulator.is_failed()
        simulator.step({"d": True})
        assert simulator.is_failed()

    @given(propositional_words(list("abcd"), min_size=0, max_size=3))
    def test_reset(self, word):
        """Test the behaviour of the method 'reset'."""
        simulator = AutomatonSimulator(self.dfa)

        assert not simulator.is_started
        assert simulator.cur_state == {self.dfa.initial_state}

        for symbol in word:
            simulator.step(symbol)
            assert simulator.is_started

        initial_state = simulator.reset()
        assert not simulator.is_started
        assert simulator.cur_state == initial_state == {self.dfa.initial_state}

    @given(propositional_words(list("abcd"), min_size=0, max_size=4))
    def test_accepts(self, word):
        """Test the behaviour of the method 'accepts'."""
        simulator = AutomatonSimulator(self.dfa)

        assert simulator.accepts(word) == self.dfa.accepts(word)

        for index, symbol in enumerate(word):
            simulator.step(symbol)
            assert simulator.accepts(word[index:]) == self.dfa.accepts(word)
