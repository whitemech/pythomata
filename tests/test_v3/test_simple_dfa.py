# -*- coding: utf-8 -*-
import pytest

from pythomata.v3.alphabets import MapAlphabet
from pythomata.v3.dfas.simple import SimpleDFA


class TestSimpleDFA:
    """Basic tests for the SimpleDFA implementation.."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.dfa = SimpleDFA(
            {0, 1, 2},
            MapAlphabet(['a', 'b', 'c']),
            0,
            {2},
            {
                0: {
                    'a': 0,
                    'b': 1,
                    'c': 2,
                },
                1: {
                    'a': 0,
                    'b': 1,
                    'c': 2,
                },
                2: {
                    'a': 0,
                    'b': 1,
                    'c': 2
                }
            }
        )

    def test_accepts(self):
        """Test the accepts work as expected."""
        assert self.dfa.accepts(['a', 'b', 'c'])
        assert not self.dfa.accepts(['a', 'b', 'c', 'a'])
        assert self.dfa.accepts(['a', 'b', 'c', 'b', 'c'])

    def test_states(self):
        """Test the set of states is correct."""
        assert self.dfa.states == {0, 1, 2}

    def test_initial_states(self):
        """Test initial states."""
        assert self.dfa.initial_states == {0}

    def test_initial_state(self):
        """Test initial states."""
        assert self.dfa.initial_state == 0

    def test_final_states(self):
        """Test initial states."""
        assert self.dfa.final_states == {2}

    def test_size(self):
        """Test size."""
        assert self.dfa.size == 3

    def test_transition_function(self):
        """Test the transition function."""
        assert self.dfa.transition_function == {
            0: {'a': 0, 'b': 1, 'c': 2},
            1: {'a': 0, 'b': 1, 'c': 2},
            2: {'a': 0, 'b': 1, 'c': 2}
        }

    def test_get_successors(self):
        """Test get successors."""
        assert self.dfa.get_successors(0, 'a') == {0}
        assert self.dfa.get_successors(0, 'b') == {1}
        assert self.dfa.get_successors(0, 'c') == {2}
        assert self.dfa.get_successors(1, 'a') == {0}
        assert self.dfa.get_successors(1, 'b') == {1}
        assert self.dfa.get_successors(1, 'c') == {2}
        assert self.dfa.get_successors(2, 'a') == {0}
        assert self.dfa.get_successors(2, 'b') == {1}
        assert self.dfa.get_successors(2, 'c') == {2}

    def test_successor_with_non_alphabet_symbol(self):
        """Test the 'get_successors' with a non-alphabet symbol."""
        assert self.dfa.get_successors(0, 'd') == {None}

    def test_is_accepting(self):
        """Test is_accepting."""
        assert not self.dfa.is_accepting(0)
        assert not self.dfa.is_accepting(1)
        assert self.dfa.is_accepting(2)


class TestPartialSimpleDFA:
    """Test a non-complete DFA."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.dfa = SimpleDFA(
            {0, 1, 2},
            MapAlphabet(['a', 'b', 'c']),
            0,
            {2},
            {
                0: {
                    'a': 0,
                    'b': 1
                },
                1: {
                    'b': 1,
                    'c': 2,
                },
                2: {
                    'c': 2
                }
            }
        )

    def test_accepts(self):
        """Test the accepts work as expected."""
        assert self.dfa.accepts(['a', 'b', 'c'])
        assert not self.dfa.accepts(['a', 'b', 'c', 'a'])
        assert not self.dfa.accepts(['a', 'b', 'c', 'b', 'c'])

    def test_transition_function(self):
        """Test the transition function."""
        assert self.dfa.transition_function == {
            0: {'a': 0, 'b': 1},
            1: {'b': 1, 'c': 2},
            2: {'c': 2}
        }

    def test_get_successors(self):
        """Test get successors."""
        assert self.dfa.get_successors(0, 'a') == {0}
        assert self.dfa.get_successors(0, 'b') == {1}
        assert self.dfa.get_successors(0, 'c') == {None}
        assert self.dfa.get_successors(1, 'a') == {None}
        assert self.dfa.get_successors(1, 'b') == {1}
        assert self.dfa.get_successors(1, 'c') == {2}
        assert self.dfa.get_successors(2, 'a') == {None}
        assert self.dfa.get_successors(2, 'b') == {None}
        assert self.dfa.get_successors(2, 'c') == {2}


class TestCheckConsistency:
    """Test suite to check the input is validated as expected."""

    def test_empty_set_of_states_raises_error(self):
        """Test that when we try to instantiate a DFA with an empty set of states we raise an error."""
        with pytest.raises(ValueError, match="The set of states cannot be empty."):
            SimpleDFA(set(), MapAlphabet({"a"}), "q0", set(), {})

    def test_initial_state_not_in_states_raises_error(self):
        """Test that if the initial state is not in the set of states we raise an error."""
        with pytest.raises(ValueError, match="Initial state .* not in the set of states."):
            SimpleDFA(set("q1"), MapAlphabet({"a"}), "q0", set(), {})

    def test_some_accepting_states_not_in_states_raises_error(self):
        """Test that if some accepting states are not in the set of states we raise an error."""
        with pytest.raises(ValueError, match="Accepting states .* not in the set of states."):
            SimpleDFA({"q0", "q1"}, MapAlphabet({"a"}), "q0", {"q2", "q3"}, {})

    def test_transition_function_with_invalid_start_states_raises_error(self):
        """Test that if some of the starting states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: states .* "
                                             "are not in the set of states."):
            SimpleDFA({"q0", "q1"}, MapAlphabet({"a"}), "q0", set(), {"q0": {"a": "q1"}, "q2": {"a": "q1"}})

    def test_transition_function_with_invalid_end_states_raises_error(self):
        """Test that if some of the ending states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: states .* "
                                             "are not in the set of states."):
            SimpleDFA({"q0", "q1"}, MapAlphabet({"a"}), "q0", set(), {"q0": {"a": "q1"},
                                                                      "q1": {"a": "q2"}})

    def test_transition_function_with_symbols_not_in_alphabet_raises_error(self):
        """Test that if a symbol of some transitions is not in the alphabet we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: symbols .* are not in the alphabet."):
            SimpleDFA({"q0", "q1"}, MapAlphabet({"a"}), "q0", set(), {"q0": {"a": "q1"},
                                                                      "q1": {"b": "q1"}})

    def test_transition_function_with_invalid_symbols_raises_error(self):
        """Test that if a symbol of some transitions is invalid we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: symbols .* are not in the alphabet."):
            SimpleDFA({"q0", "q1"}, MapAlphabet({"a"}), "q0", set(), {"q0": {"a": "q1"},
                                                         "q1": {"b": "q1"}})
