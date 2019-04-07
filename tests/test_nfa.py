# -*- coding: utf-8 -*-
import pytest

from pythomata.nfa import NFA


class TestNFA:
    """Basic tests for the NFA class."""

    def test_instantiate_nfa(self):
        """Test that we can instantiate a simple NFA."""
        nfa = NFA(
            {"q0", "q1", "q2"},
            {"a0", "a1"},
            "q0",
            {"q2"},
            {
                "q0": {
                    "a0": {"q1"}
                },
                "q1": {
                    "a1": {"q2"}
                },
            }
        )

    def test_equality(self):
        """Test that the equality between two NFA works correctly."""

        nfa_1 = NFA(
            {"q0"},
            {"a0"},
            "q0",
            set(),
            {}
        )

        nfa_2 = NFA(
            {"q0"},
            {"a0"},
            "q0",
            set(),
            {}
        )

        assert nfa_1 == nfa_2
        assert nfa_1 != tuple()

    def test_nfa_from_transitions(self):
        """Test that the constructor "from_transitions" works correctly."""

        states = {"q0", "q1", "q2"}
        actions = {"a0", "a1"}
        initial_state = "q0"
        final_states = {"q2"}
        transition_function = {"q0": {"a0":  {"q1", "q2"}}, "q1": {"a1": {"q2"}}}

        expected_nfa = NFA(
            states,
            actions,
            initial_state,
            final_states,
            transition_function
        )

        actual_nfa = NFA.from_transitions(initial_state, final_states, transition_function)

        assert expected_nfa == actual_nfa


class TestCheckConsistency:
    """Test suite to check the input is validated as expected."""

    def test_if_use_reserved_state_names_raises_error(self):
        """Test that when we try to instantiate a NFA with reserved state names we raise an error."""
        with pytest.raises(ValueError, match="The following state names are reserved or invalid: .*"):
            nfa = NFA({""}, {"a"}, "q0", set(), {})

    def test_if_use_reserved_symbol_names_raises_error(self):
        """Test that when we try to instantiate a NFA with reserved symbol names we raise an error."""
        with pytest.raises(ValueError, match="The following symbol names are reserved or invalid: .*"):
            nfa = NFA(set("q0"), {""}, "q0", set(), {})

    def test_empty_set_of_states_raises_error(self):
        """Test that when we try to instantiate a NFA with an empty set of states we raise an error."""
        with pytest.raises(ValueError, match="The set of states cannot be empty."):
            nfa = NFA(set(), {"a"}, "q0", set(), {})

    def test_initial_state_not_in_states_raises_error(self):
        """Test that if the initial state is not in the set of states we raise an error."""
        with pytest.raises(ValueError, match="Initial state .* not in the set of states."):
            nfa = NFA(set("q1"), {"a"}, "q0", set(), {})

    def test_some_accepting_states_not_in_states_raises_error(self):
        """Test that if some accepting states are not in the set of states we raise an error."""
        with pytest.raises(ValueError, match="Accepting states .* not in the set of states."):
            nfa = NFA({"q0", "q1"}, {"a"}, "q0", {"q2", "q3"}, {})

    def test_transition_function_with_invalid_start_states_raises_error(self):
        """Test that if some of the starting states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: states .* "
                                             "are not in the set of states."):
            nfa = NFA({"q0", "q1"}, {"a"}, "q0", set(), {"q0": {"a": {"q1"}}, "q2": {"a": {"q1"}}})

    def test_transition_function_with_invalid_end_states_raises_error(self):
        """Test that if some of the ending states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: states .* "
                                             "are not in the set of states."):
            nfa = NFA({"q0", "q1"}, {"a"}, "q0", set(), {"q0": {"a": {"q1"}},
                                                         "q1": {"a": {"q2"}}})

    def test_transition_function_with_symbols_not_in_alphabet_raises_error(self):
        """Test that if a symbol of some transitions is not in the alphabet we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: symbols .* are not in the alphabet."):
            nfa = NFA({"q0", "q1"}, {"a"}, "q0", set(), {"q0": {"a": {"q1"}},
                                                         "q1": {"b": {"q1"}}})

    def test_transition_function_with_invalid_symbols_raises_error(self):
        """Test that if a symbol of some transitions is invalid we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: symbols .* are not in the alphabet."):
            nfa = NFA({"q0", "q1"}, {"a"}, "q0", set(), {"q0": {"a": {"q1"}},
                                                         "q1": {"b": {"q1"}}})

    def test_transition_function_with_invalid_state_names_raises_error(self):
        """Test that if a state name of some transitions is invalid we raise an error."""
        with pytest.raises(ValueError, match="The following state names are reserved or invalid: .*"):
            nfa = NFA({"", "q1"}, {"a"}, "q0", set(), {"": {"a": {"q1"}},
                                                       "q1": {"b": {"q1"}}})


class TestDeterminize:

    def test_determinize(self):

        nfa = NFA(
            {"q0", "q1", "q2", "q3"},
            {"a", "b"},
            "q0",
            {"q3"},
            {
                "q0": {
                    "a": {"q1"}
                },
                "q1": {
                    "a": {"q0"},
                    "b": {"q2", "q1"}
                },
                "q2": {
                    "a": {"q2"},
                    "b": {"q3"}
                }
            }
        )

        actual_dfa = nfa.determinize().trim().minimize()

        assert not actual_dfa.accepts([])
        assert not actual_dfa.accepts(["a"])
        assert not actual_dfa.accepts(["b"])
        assert not actual_dfa.accepts(["a", "a"])
        assert not actual_dfa.accepts(["a", "b", "a"])
        assert not actual_dfa.accepts(["a", "a", "a", "b"])
        assert actual_dfa.accepts(["a", "a", "a", "b", "b", "a", "b"])


class TestToDot:

    def test_to_dot(self):

        nfa = NFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            {"a", "b"},
            "q0",
            {"q0"},
            {}
        )

        nfa.to_dot("./tmp/dfa", title="test dfa (initial state final)")

        nfa = NFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            {"a", "b"},
            "q0",
            {"q3"},
            {"q0": {"a": {"q0"}, "b": {"q1"}},
             "q1": {"a": {"q0"}, "b": {"q2"}},
             "q2": {"a": {"q3"}, "b": {"q4"}},
             "q3": {"a": {"q3"}, "b": {"q4"}},
             "q4": {"a": {"q3"}, "b": {"q5"}}}
        )

        nfa.to_dot("./tmp/dfa", title="test dfa")

