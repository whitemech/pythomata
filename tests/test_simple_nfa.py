# -*- coding: utf-8 -*-
import pytest

from pythomata.alphabets import MapAlphabet
from pythomata.impl.simple import SimpleNFA


class TestNFA:
    """Basic tests for the NFA class."""

    def test_instantiate_nfa(self):
        """Test that we can instantiate a simple NFA."""
        nfa = SimpleNFA(
            {"q0", "q1", "q2"},
            {"a0", "a1"},
            "q0",
            {"q2"},
            {"q0": {"a0": {"q1"}}, "q1": {"a1": {"q2"}}},
        )

    def test_equality(self):
        """Test that the equality between two NFA works correctly."""

        nfa_1 = SimpleNFA({"q0"}, {"a0"}, "q0", set(), {})

        nfa_2 = SimpleNFA({"q0"}, {"a0"}, "q0", set(), {})

        assert nfa_1 == nfa_2
        assert nfa_1 != tuple()

    def test_nfa_from_transitions(self):
        """Test that the constructor "from_transitions" works correctly."""

        states = {"q0", "q1", "q2"}
        actions = MapAlphabet({"a0", "a1"})
        initial_state = "q0"
        final_states = {"q2"}
        transition_function = {"q0": {"a0": {"q1", "q2"}}, "q1": {"a1": {"q2"}}}

        expected_nfa = SimpleNFA(
            states, actions, initial_state, final_states, transition_function
        )

        actual_nfa = SimpleNFA.from_transitions(
            initial_state, final_states, transition_function
        )

        assert expected_nfa == actual_nfa


class TestCheckConsistency:
    """Test suite to check the input is validated as expected."""

    def test_empty_set_of_states_raises_error(self):
        """Test that when we try to instantiate a NFA with an empty set of states we raise an error."""
        with pytest.raises(ValueError, match="The set of states cannot be empty."):
            nfa = SimpleNFA(set(), MapAlphabet({"a"}), "q0", set(), {})

    def test_initial_state_not_in_states_raises_error(self):
        """Test that if the initial state is not in the set of states we raise an error."""
        with pytest.raises(
            ValueError, match="Initial state .* not in the set of states."
        ):
            nfa = SimpleNFA(set("q1"), MapAlphabet({"a"}), "q0", set(), {})

    def test_some_accepting_states_not_in_states_raises_error(self):
        """Test that if some accepting states are not in the set of states we raise an error."""
        with pytest.raises(
            ValueError, match="Accepting states .* not in the set of states."
        ):
            nfa = SimpleNFA({"q0", "q1"}, MapAlphabet({"a"}), "q0", {"q2", "q3"}, {})

    def test_transition_function_with_invalid_start_states_raises_error(self):
        """Test that if some of the starting states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(
            ValueError,
            match="Transition function not valid: states .* "
            "are not in the set of states.",
        ):
            nfa = SimpleNFA(
                {"q0", "q1"},
                MapAlphabet({"a"}),
                "q0",
                set(),
                {"q0": {"a": {"q1"}}, "q2": {"a": {"q1"}}},
            )

    def test_transition_function_with_invalid_end_states_raises_error(self):
        """Test that if some of the ending states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(
            ValueError,
            match="Transition function not valid: states .* "
            "are not in the set of states.",
        ):
            nfa = SimpleNFA(
                {"q0", "q1"},
                MapAlphabet({"a"}),
                "q0",
                set(),
                {"q0": {"a": {"q1"}}, "q1": {"a": {"q2"}}},
            )

    def test_transition_function_with_symbols_not_in_alphabet_raises_error(self):
        """Test that if a symbol of some transitions is not in the alphabet we raise an error."""
        with pytest.raises(
            ValueError,
            match="Transition function not valid: some symbols are not in the alphabet.",
        ):
            nfa = SimpleNFA(
                {"q0", "q1"},
                MapAlphabet({"a"}),
                "q0",
                set(),
                {"q0": {"a": {"q1"}}, "q1": {"b": {"q1"}}},
            )

    def test_transition_function_with_invalid_symbols_raises_error(self):
        """Test that if a symbol of some transitions is invalid we raise an error."""
        with pytest.raises(
            ValueError,
            match="Transition function not valid: some symbols are not in the alphabet.",
        ):
            nfa = SimpleNFA(
                {"q0", "q1"},
                MapAlphabet({"a"}),
                "q0",
                set(),
                {"q0": {"a": {"q1"}}, "q1": {"b": {"q1"}}},
            )


class TestDeterminize:
    def test_determinize(self):

        nfa = SimpleNFA(
            {"q0", "q1", "q2", "q3"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q3"},
            {
                "q0": {"a": {"q1"}},
                "q1": {"a": {"q0"}, "b": {"q2", "q1"}},
                "q2": {"a": {"q2"}, "b": {"q3"}},
            },
        )

        actual_dfa = nfa.determinize().minimize().trim()

        assert not actual_dfa.accepts([])
        assert not actual_dfa.accepts(["a"])
        assert not actual_dfa.accepts(["b"])
        assert not actual_dfa.accepts(["a", "a"])
        assert not actual_dfa.accepts(["a", "b", "a"])
        assert not actual_dfa.accepts(["a", "a", "a", "b"])
        assert actual_dfa.accepts(["a", "a", "a", "b", "b", "a", "b"])


class TestToGraphviz:
    def test_to_graphviz(self):

        nfa = SimpleNFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q0"},
            {},
        )

        nfa.to_graphviz()

        nfa = SimpleNFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            MapAlphabet({"a", "b"}),
            "q0",
            {"q3"},
            {
                "q0": {"a": {"q0"}, "b": {"q1"}},
                "q1": {"a": {"q0"}, "b": {"q2"}},
                "q2": {"a": {"q3"}, "b": {"q4"}},
                "q3": {"a": {"q3"}, "b": {"q4"}},
                "q4": {"a": {"q3"}, "b": {"q5"}},
            },
        )

        nfa.to_graphviz()
