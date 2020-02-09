# -*- coding: utf-8 -*-
from functools import reduce

import pytest
from hypothesis import given

from pythomata import SimpleDFA
from pythomata.alphabets import MapAlphabet, ArrayAlphabet
from pythomata.impl.simple import EmptyDFA
from pythomata.simulator import AutomatonSimulator
from tests.strategies import simple_words


class TestSimpleDFA:
    """Basic tests for the SimpleDFA implementation.."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.dfa = SimpleDFA(
            {0, 1, 2},
            ["a", "b", "c"],
            0,
            {2},
            {
                0: {"a": 0, "b": 1, "c": 2},
                1: {"a": 0, "b": 1, "c": 2},
                2: {"a": 0, "b": 1, "c": 2},
            },
        )

    def test_accepts(self):
        """Test the accepts work as expected."""
        assert self.dfa.accepts(["a", "b", "c"])
        assert not self.dfa.accepts(["a", "b", "c", "a"])
        assert self.dfa.accepts(["a", "b", "c", "b", "c"])

    def test_states(self):
        """Test the set of states is correct."""
        assert self.dfa.states == {0, 1, 2}

    def test_initial_state(self):
        """Test initial state."""
        assert self.dfa.initial_state == 0

    def test_final_states(self):
        """Test initial states."""
        assert self.dfa.accepting_states == {2}

    def test_size(self):
        """Test size."""
        assert self.dfa.size == 3

    def test_transition_function(self):
        """Test the transition function."""
        assert self.dfa.transition_function == {
            0: {"a": 0, "b": 1, "c": 2},
            1: {"a": 0, "b": 1, "c": 2},
            2: {"a": 0, "b": 1, "c": 2},
        }

    def test_get_successors(self):
        """Test get successors."""
        assert self.dfa.get_successors(0, "a") == {0}
        assert self.dfa.get_successors(0, "b") == {1}
        assert self.dfa.get_successors(0, "c") == {2}
        assert self.dfa.get_successors(1, "a") == {0}
        assert self.dfa.get_successors(1, "b") == {1}
        assert self.dfa.get_successors(1, "c") == {2}
        assert self.dfa.get_successors(2, "a") == {0}
        assert self.dfa.get_successors(2, "b") == {1}
        assert self.dfa.get_successors(2, "c") == {2}

    def test_successor_with_non_alphabet_symbol(self):
        """Test the 'get_successors' with a non-alphabet symbol."""
        assert self.dfa.get_successors(0, "d") == set()

    def test_is_accepting(self):
        """Test is_accepting."""
        assert not self.dfa.is_accepting(0)
        assert not self.dfa.is_accepting(1)
        assert self.dfa.is_accepting(2)

    def test_equality(self):
        """Test that the equality between two SimpleDFA works correctly."""
        assert self.dfa == self.dfa

        another_dfa = SimpleDFA(
            {0, 1, 2},
            MapAlphabet(["a", "b", "c"]),
            0,
            {2},
            {
                0: {"a": 0, "b": 1, "c": 2},
                1: {"a": 0, "b": 1, "c": 2},
                2: {"a": 0, "b": 1, "c": 2},
            },
        )
        assert self.dfa == another_dfa


class TestPartialSimpleDFA:
    """Test a non-complete DFA."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.dfa = SimpleDFA(
            {0, 1, 2},
            MapAlphabet(["a", "b", "c"]),
            0,
            {2},
            {0: {"a": 0, "b": 1}, 1: {"b": 1, "c": 2}, 2: {"c": 2}},
        )

    def test_accepts(self):
        """Test the accepts work as expected."""
        assert self.dfa.accepts(["a", "b", "c"])
        assert not self.dfa.accepts(["a", "b", "c", "a"])
        assert not self.dfa.accepts(["a", "b", "c", "b", "c"])

    def test_transition_function(self):
        """Test the transition function."""
        assert self.dfa.transition_function == {
            0: {"a": 0, "b": 1},
            1: {"b": 1, "c": 2},
            2: {"c": 2},
        }

    def test_get_successors(self):
        """Test get successors."""
        assert self.dfa.get_successors(0, "a") == {0}
        assert self.dfa.get_successors(0, "b") == {1}
        assert self.dfa.get_successors(0, "c") == set()
        assert self.dfa.get_successors(1, "a") == set()
        assert self.dfa.get_successors(1, "b") == {1}
        assert self.dfa.get_successors(1, "c") == {2}
        assert self.dfa.get_successors(2, "a") == set()
        assert self.dfa.get_successors(2, "b") == set()
        assert self.dfa.get_successors(2, "c") == {2}


class TestCheckConsistency:
    """Test suite to check the input is validated as expected."""

    def test_empty_set_of_states_raises_error(self):
        """Test that when we try to instantiate a DFA with an empty set of states we raise an error."""
        with pytest.raises(ValueError, match="The set of states cannot be empty."):
            SimpleDFA(set(), MapAlphabet({"a"}), "q0", set(), {})

    def test_initial_state_not_in_states_raises_error(self):
        """Test that if the initial state is not in the set of states we raise an error."""
        with pytest.raises(
            ValueError, match="Initial state .* not in the set of states."
        ):
            SimpleDFA(set("q1"), MapAlphabet({"a"}), "q0", set(), {})

    def test_some_accepting_states_not_in_states_raises_error(self):
        """Test that if some accepting states are not in the set of states we raise an error."""
        with pytest.raises(
            ValueError, match="Accepting states .* not in the set of states."
        ):
            SimpleDFA({"q0", "q1"}, MapAlphabet({"a"}), "q0", {"q2", "q3"}, {})

    def test_transition_function_with_invalid_start_states_raises_error(self):
        """Test that if some of the starting states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(
            ValueError,
            match="Transition function not valid: states .* "
            "are not in the set of states.",
        ):
            SimpleDFA(
                {"q0", "q1"},
                MapAlphabet({"a"}),
                "q0",
                set(),
                {"q0": {"a": "q1"}, "q2": {"a": "q1"}},
            )

    def test_transition_function_with_invalid_end_states_raises_error(self):
        """Test that if some of the ending states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(
            ValueError,
            match="Transition function not valid: states .* "
            "are not in the set of states.",
        ):
            SimpleDFA(
                {"q0", "q1"},
                MapAlphabet({"a"}),
                "q0",
                set(),
                {"q0": {"a": "q1"}, "q1": {"a": "q2"}},
            )

    def test_transition_function_with_symbols_not_in_alphabet_raises_error(self):
        """Test that if a symbol of some transitions is not in the alphabet we raise an error."""
        with pytest.raises(
            ValueError,
            match="Transition function not valid: symbols .* are not in the alphabet.",
        ):
            SimpleDFA(
                {"q0", "q1"},
                MapAlphabet({"a"}),
                "q0",
                set(),
                {"q0": {"a": "q1"}, "q1": {"b": "q1"}},
            )

    def test_transition_function_with_invalid_symbols_raises_error(self):
        """Test that if a symbol of some transitions is invalid we raise an error."""
        with pytest.raises(
            ValueError,
            match="Transition function not valid: symbols .* are not in the alphabet.",
        ):
            SimpleDFA(
                {"q0", "q1"},
                MapAlphabet({"a"}),
                "q0",
                set(),
                {"q0": {"a": "q1"}, "q1": {"b": "q1"}},
            )


def test_dfa_from_transitions():
    """Test that the constructor "from_transitions" works correctly."""

    states = {"q0", "q1", "q2"}
    actions = MapAlphabet({"a0", "a1"})
    initial_state = "q0"
    final_states = {"q2"}
    transition_function = {"q0": {"a0": "q1"}, "q1": {"a1": "q2"}}

    expected_dfa = SimpleDFA(
        states, actions, initial_state, final_states, transition_function
    )

    actual_dfa = SimpleDFA.from_transitions(
        initial_state, final_states, transition_function
    )

    assert expected_dfa == actual_dfa


class TestIsComplete:
    def test_is_complete_when_dfa_is_complete(self):
        """Test that the is_complete method return True if the SimpleDFA is complete."""
        dfa = SimpleDFA({"q"}, MapAlphabet({"a"}), "q", set(), {"q": {"a": "q"}})
        assert dfa.is_complete()

    def test_is_complete_when_dfa_is_not_complete(self):
        """Test that the is_complete method return False if the SimpleDFA is not complete."""
        dfa = SimpleDFA(
            {"q0", "q1"},
            MapAlphabet({"a", "b"}),
            "q0",
            set(),
            {"q0": {"a": "q0", "b": "q1"}},
        )
        assert not dfa.is_complete()


class TestComplete:
    def test_complete_when_dfa_is_already_complete(self):
        """Test that when we try to make complete an already complete SimpleDFA
        then the returned SimpleDFA is equal to the previous one."""

        complete_dfa = SimpleDFA(
            {"q"}, MapAlphabet({"a"}), "q", set(), {"q": {"a": "q"}}
        )

        new_dfa = complete_dfa.complete()
        assert complete_dfa == new_dfa

    def test_complete_when_dfa_is_not_complete(self):
        """Test that when we try to make complete a non-complete SimpleDFA
        then the returned SimpleDFA is complete."""

        dfa = SimpleDFA(
            {"q0", "q1"},
            MapAlphabet({"a", "b"}),
            "q0",
            set(),
            {"q0": {"a": "q0", "b": "q1"}},
        )

        expected_dfa = SimpleDFA(
            {"q0", "q1", "sink"},
            MapAlphabet({"a", "b"}),
            "q0",
            set(),
            {
                "q0": {"a": "q0", "b": "q1"},
                "q1": {"a": "sink", "b": "sink"},
                "sink": {"a": "sink", "b": "sink"},
            },
        )

        actual_dfa = dfa.complete()
        assert actual_dfa == expected_dfa


class TestMinimize:
    def test_minimize(self):

        dfa = SimpleDFA(
            {"q0", "q1", "q2", "q3", "q4"},
            MapAlphabet({"a", "b", "c"}),
            "q0",
            {"q3", "q4"},
            {
                "q0": {"a": "q1", "b": "q2"},
                "q1": {"c": "q3"},
                "q2": {"c": "q3"},
                "q3": {"c": "q4"},
                "q4": {"c": "q4"},
            },
        )

        actual_minimized_dfa = dfa.minimize()

        # the renaming of the states is non deterministic, so we need to compare every substructure.
        assert len(actual_minimized_dfa._states) == 4
        assert actual_minimized_dfa._alphabet == ArrayAlphabet(["a", "b", "c"])
        assert actual_minimized_dfa.is_complete()

    def test_every_minimized_dfa_is_complete(self):
        """Test that every minimized SimpleDFA is complete."""
        # TODO use Hypothesis
        pass


class TestReachable:
    def test_reachable_simple_case(self):

        dfa = SimpleDFA(
            {"q0", "q1", "q2"},
            MapAlphabet({"a1", "a2"}),
            "q0",
            {"q0"},
            {"q0": {"a1": "q0", "a2": "q1"}},
        )

        actual_reachable = dfa.reachable()

        expected_reachable = SimpleDFA(
            {"q0", "q1"},
            MapAlphabet({"a1", "a2"}),
            "q0",
            {"q0"},
            {"q0": {"a1": "q0", "a2": "q1"}},
        )

        assert actual_reachable == expected_reachable

    def test_reachable_no_transitions(self):
        """Test that the reachable SimpleDFA of a SimpleDFA without transitions
        is the SimpleDFA with only the initial state."""

        dfa = SimpleDFA({"q0", "q1", "q2"}, MapAlphabet({"a1", "a2"}), "q0", {"q1"}, {})

        actual_reachable_dfa = dfa.reachable()
        expected_reachable_dfa = SimpleDFA(
            {"q0"}, MapAlphabet({"a1", "a2"}), "q0", set(), {}
        )

        assert actual_reachable_dfa == expected_reachable_dfa


class TestCoReachable:
    def test_coreachable_simple_case(self):

        dfa = SimpleDFA(
            {"q0", "q1", "q2"},
            MapAlphabet({"a1", "a2"}),
            "q0",
            {"q0"},
            {"q0": {"a1": "q0", "a2": "q1"}},
        )

        actual_coreachable = dfa.coreachable()

        expected_coreachable = SimpleDFA(
            {"q0"}, MapAlphabet({"a1", "a2"}), "q0", {"q0"}, {"q0": {"a1": "q0"}}
        )

        assert actual_coreachable == expected_coreachable

    def test_coreachable_no_accepting_states_gives_empty_dfa(self):

        dfa = SimpleDFA(
            {"q0", "q1", "q2"},
            MapAlphabet({"a1", "a2"}),
            "q0",
            set(),
            {"q0": {"a1": "q0", "a2": "q1"}},
        )

        actual_coreachable = dfa.coreachable()

        expected_coreachable = EmptyDFA(MapAlphabet({"a1", "a2"}))

        assert actual_coreachable == expected_coreachable


class TestTrim:
    def test_trim_simple_case(self):
        dfa = SimpleDFA(
            {"q0", "q1", "q2", "sink"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q1"},
            {
                "q0": {"a": "q0", "b": "q1"},
                "q1": {"a": "sink", "b": "sink"},
                "sink": {"a": "sink", "b": "sink"},
            },
        )

        actual_trimmed_dfa = dfa.trim()

        expected_trimmed_dfa = SimpleDFA(
            {"q0", "q1"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q1"},
            {"q0": {"a": "q0", "b": "q1"}},
        )

        assert actual_trimmed_dfa == expected_trimmed_dfa


class TestAccepts:
    def test_accepts(self):

        dfa = SimpleDFA(
            {"q0", "q1"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q1"},
            {"q0": {"a": "q0", "b": "q1"}},
        )

        assert not dfa.accepts([])
        assert not dfa.accepts(["a"])
        assert not dfa.accepts(["a"])
        assert dfa.accepts(["b"])
        assert dfa.accepts(["a", "b"])
        assert not dfa.accepts(["a", "a"])
        assert not dfa.accepts(["b", "b"])


class TestLevelToAcceptingStates:
    def test_level_to_accepting_states(self):
        dfa = SimpleDFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q3"},
            {
                "q0": {"a": "q0", "b": "q1"},
                "q1": {"a": "q0", "b": "q2"},
                "q2": {"a": "q3", "b": "q4"},
                "q3": {"a": "q3", "b": "q4"},
                "q4": {"a": "q3", "b": "q5"},
            },
        )

        assert dfa.levels_to_accepting_states() == {
            "q0": 3,
            "q1": 2,
            "q2": 1,
            "q3": 0,
            "q4": 1,
            "q5": -1,
        }


class TestToGraphviz:
    """Test the 'to_graphviz' method."""

    def test_to_graphviz(self):

        dfa = SimpleDFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q0"},
            {},
        )

        dfa.to_graphviz()

        dfa = SimpleDFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q3"},
            {
                "q0": {"a": "q0", "b": "q1"},
                "q1": {"a": "q0", "b": "q2"},
                "q2": {"a": "q3", "b": "q4"},
                "q3": {"a": "q3", "b": "q4"},
                "q4": {"a": "q3", "b": "q5"},
            },
        )

        dfa.to_graphviz()


class TestSimulator:
    """Test the simulator with a SimpleDFA"""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.dfa = SimpleDFA(
            {0, 1, 2},
            MapAlphabet(["a", "b", "c", "d"]),
            0,
            {2},
            {
                0: {"a": 0, "b": 1, "c": 2},
                1: {"a": 0, "b": 1, "c": 2},
                2: {"a": 0, "b": 1, "c": 2},
            },
        )

    def test_initialization(self):
        """Test the initialization of a simulator."""
        simulator = AutomatonSimulator(self.dfa)

        assert simulator.automaton == self.dfa
        assert simulator.cur_state == {self.dfa.initial_state}
        assert not simulator.is_started

    @given(simple_words(list("abcd"), min_size=0, max_size=5))
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
        simulator.step("a")
        assert not simulator.is_true()
        simulator.step("b")
        assert not simulator.is_true()
        simulator.step("c")
        assert simulator.is_true()

    def test_is_failed(self):
        """Test the behaviour of the method 'is_failed'."""
        simulator = AutomatonSimulator(self.dfa)

        assert not simulator.is_failed()
        simulator.step("a")
        assert not simulator.is_failed()
        simulator.step("b")
        assert not simulator.is_failed()
        simulator.step("c")
        assert not simulator.is_failed()
        simulator.step("d")
        assert simulator.is_failed()

    @given(simple_words(list("abcd"), min_size=0, max_size=3))
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

    @given(simple_words(list("abcd"), min_size=0, max_size=10))
    def test_accepts(self, word):
        """Test the behaviour of the method 'accepts'."""
        simulator = AutomatonSimulator(self.dfa)

        assert simulator.accepts(word) == self.dfa.accepts(word)

        for index, symbol in enumerate(word):
            simulator.step(symbol)
            assert simulator.accepts(word[index:]) == self.dfa.accepts(word)
