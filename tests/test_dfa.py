
import pytest

from pythomata.dfa import DFA, EmptyDFA


class TestDFA:
    """Basic tests for the DFA class."""

    def test_instantiate_dfa(self):
        """Test that we can instantiate a simple DFA."""
        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a0", "a1"},
            "q0",
            {"q2"},
            {
                "q0": {
                    "a0": "q1"
                },
                "q1": {
                    "a1": "q2"
                },
            }
        )

    def test_equality(self):
        """Test that the equality between two DFA works correctly."""

        dfa_1 = DFA(
            {"q0"},
            {"a0"},
            "q0",
            set(),
            {}
        )

        dfa_2 = DFA(
            {"q0"},
            {"a0"},
            "q0",
            set(),
            {}
        )

        assert dfa_1 == dfa_2
        assert dfa_1 != tuple()

    def test_dfa_from_transitions(self):
        """Test that the constructor "from_transitions" works correctly."""

        states = {"q0", "q1", "q2"}
        actions = {"a0", "a1"}
        initial_state = "q0"
        final_states = {"q2"}
        transition_function = {"q0": {"a0": "q1"}, "q1": {"a1": "q2"}}

        expected_dfa = DFA(
            states,
            actions,
            initial_state,
            final_states,
            transition_function
        )

        actual_dfa = DFA.from_transitions(initial_state, final_states, transition_function)

        assert expected_dfa == actual_dfa


class TestCheckConsistency:
    """Test suite to check the input is validated as expected."""

    def test_if_use_reserved_state_names_raises_error(self):
        """Test that when we try to instantiate a DFA with reserved state names we raise an error."""
        with pytest.raises(ValueError, match="The following state names are reserved or invalid: .*"):
            dfa = DFA({""}, {"a"}, "q0", set(), {})

    def test_if_use_reserved_symbol_names_raises_error(self):
        """Test that when we try to instantiate a DFA with reserved symbol names we raise an error."""
        with pytest.raises(ValueError, match="The following symbol names are reserved or invalid: .*"):
            dfa = DFA(set("q0"), {""}, "q0", set(), {})

    def test_empty_set_of_states_raises_error(self):
        """Test that when we try to instantiate a DFA with an empty set of states we raise an error."""
        with pytest.raises(ValueError, match="The set of states cannot be empty."):
            dfa = DFA(set(), {"a"}, "q0", set(), {})

    def test_initial_state_not_in_states_raises_error(self):
        """Test that if the initial state is not in the set of states we raise an error."""
        with pytest.raises(ValueError, match="Initial state .* not in the set of states."):
            dfa = DFA(set("q1"), {"a"}, "q0", set(), {})

    def test_some_accepting_states_not_in_states_raises_error(self):
        """Test that if some accepting states are not in the set of states we raise an error."""
        with pytest.raises(ValueError, match="Accepting states .* not in the set of states."):
            dfa = DFA({"q0", "q1"}, {"a"}, "q0", {"q2", "q3"}, {})

    def test_transition_function_with_invalid_start_states_raises_error(self):
        """Test that if some of the starting states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: states .* "
                                             "are not in the set of states."):
            dfa = DFA({"q0", "q1"}, {"a"}, "q0", set(), {"q0": {"a": "q1"}, "q2": {"a": "q1"}})

    def test_transition_function_with_invalid_end_states_raises_error(self):
        """Test that if some of the ending states of the transitions is not in
         the set of states we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: states .* "
                                             "are not in the set of states."):
            dfa = DFA({"q0", "q1"}, {"a"}, "q0", set(), {"q0": {"a": "q1"},
                                                         "q1": {"a": "q2"}})

    def test_transition_function_with_symbols_not_in_alphabet_raises_error(self):
        """Test that if a symbol of some transitions is not in the alphabet we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: symbols .* are not in the alphabet."):
            dfa = DFA({"q0", "q1"}, {"a"}, "q0", set(), {"q0": {"a": "q1"},
                                                         "q1": {"b": "q1"}})

    def test_transition_function_with_invalid_symbols_raises_error(self):
        """Test that if a symbol of some transitions is invalid we raise an error."""
        with pytest.raises(ValueError, match="Transition function not valid: symbols .* are not in the alphabet."):
            dfa = DFA({"q0", "q1"}, {"a"}, "q0", set(), {"q0": {"a": "q1"},
                                                         "q1": {"b": "q1"}})

    def test_transition_function_with_invalid_state_names_raises_error(self):
        """Test that if a state name of some transitions is invalid we raise an error."""
        with pytest.raises(ValueError, match="The following state names are reserved or invalid: .*"):
            dfa = DFA({"", "q1"}, {"a"}, "q0", set(), {"": {"a": "q1"},
                                                       "q1": {"b": "q1"}})


class TestIsComplete:

    def test_is_complete_when_dfa_is_complete(self):
        """Test that the is_complete method return True if the DFA is complete."""
        dfa = DFA(
            {"q"},
            {"a"},
            "q",
            set(),
            {"q": {"a": "q"}}
        )
        assert dfa.is_complete()

    def test_is_complete_when_dfa_is_not_complete(self):
        """Test that the is_complete method return False if the DFA is not complete."""
        dfa = DFA(
            {"q0", "q1"},
            {"a", "b"},
            "q0",
            set(),
            {"q0": {"a": "q0", "b": "q1"}}
        )
        assert not dfa.is_complete()


class TestComplete:

    def test_complete_when_dfa_is_already_complete(self):
        """Test that when we try to make complete an already complete DFA
        then the returned DFA is equal to the previous one."""

        complete_dfa = DFA(
            {"q"},
            {"a"},
            "q",
            set(),
            {"q": {"a": "q"}}
        )

        new_dfa = complete_dfa.complete()
        assert complete_dfa == new_dfa

    def test_complete_when_dfa_is_not_complete(self):
        """Test that when we try to make complete a non-complete DFA
        then the returned DFA is complete."""

        dfa = DFA(
            {"q0", "q1"},
            {"a", "b"},
            "q0",
            set(),
            {"q0": {"a": "q0", "b": "q1"}}
        )

        expected_dfa = DFA(
            {"q0", "q1", "sink"},
            {"a", "b"},
            "q0",
            set(),
            {"q0": {"a": "q0", "b": "q1"},
             "q1": {"a": "sink", "b": "sink"},
             "sink": {"a": "sink", "b": "sink"}}
        )

        actual_dfa = dfa.complete()
        assert actual_dfa == expected_dfa


class TestMinimize:

    def test_minimize(self):

        dfa = DFA(
            {"q0", "q1", "q2", "q3", "q4"},
            {"a", "b", "c"},
            "q0",
            {"q3", "q4"},
            {
                "q0": {
                    "a": "q1",
                    "b": "q2",
                },
                "q1": {
                    "c": "q3"
                },
                "q2": {
                    "c": "q3"
                },
                "q3": {
                    "c": "q4"
                },
                "q4": {
                    "c": "q4"
                }
            }
        )

        actual_minimized_dfa = dfa.minimize()

        # the renaming of the states is non deterministic, so we need to compare every substructure.
        assert len(actual_minimized_dfa._states) == 4
        assert actual_minimized_dfa._alphabet == {"a", "b", "c"}
        assert actual_minimized_dfa.is_complete()

    def test_every_minimized_dfa_is_complete(self):
        """Test that every minimized DFA is complete."""
        # TODO use Hypothesis
        pass


class TestReachable:

    def test_reachable_simple_case(self):

        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a1", "a2"},
            "q0",
            {"q0"},
            {"q0": {"a1": "q0", "a2": "q1"}}
        )

        actual_reachable = dfa.reachable()

        expected_reachable = DFA(
            {"q0", "q1"},
            {"a1", "a2"},
            "q0",
            {"q0"},
            {"q0": {"a1": "q0", "a2": "q1"}}
        )

        assert actual_reachable == expected_reachable

    def test_reachable_no_transitions(self):
        """Test that the reachable DFA of a DFA without transitions
        is the DFA with only the initial state."""

        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a1", "a2"},
            "q0",
            {"q1"},
            {}
        )

        actual_reachable_dfa = dfa.reachable()
        expected_reachable_dfa = DFA(
            {"q0"},
            {"a1", "a2"},
            "q0",
            set(),
            {}
        )

        assert actual_reachable_dfa == expected_reachable_dfa


class TestCoReachable:

    def test_coreachable_simple_case(self):

        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a1", "a2"},
            "q0",
            {"q0"},
            {"q0": {"a1": "q0", "a2": "q1"}}
        )

        actual_coreachable = dfa.coreachable()

        expected_coreachable = DFA(
            {"q0"},
            {"a1", "a2"},
            "q0",
            {"q0"},
            {"q0": {"a1": "q0"}}
        )

        assert actual_coreachable == expected_coreachable

    def test_coreachable_no_accepting_states_gives_empty_dfa(self):

        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a1", "a2"},
            "q0",
            set(),
            {"q0": {"a1": "q0", "a2": "q1"}}
        )

        actual_coreachable = dfa.coreachable()

        expected_coreachable = EmptyDFA()

        assert actual_coreachable == expected_coreachable


class TestTrim:

    def test_trim_simple_case(self):
        dfa = DFA(
            {"q0", "q1", "q2", "sink"},
            {"a", "b"},
            "q0",
            {"q1"},
            {"q0": {"a": "q0", "b": "q1"},
             "q1": {"a": "sink", "b": "sink"},
             "sink": {"a": "sink", "b": "sink"}}
        )

        actual_trimmed_dfa = dfa.trim()

        expected_trimmed_dfa = DFA(
            {"q0", "q1"},
            {"a", "b"},
            "q0",
            {"q1"},
            {"q0": {"a": "q0", "b": "q1"}}
        )

        assert actual_trimmed_dfa == expected_trimmed_dfa


class TestAccepts:

    def test_accepts(self):

        dfa = DFA(
            {"q0", "q1"},
            {"a", "b"},
            "q0",
            {"q1"},
            {"q0": {"a": "q0", "b": "q1"}}
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
        dfa = DFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            {"a", "b"},
            "q0",
            {"q3"},
            {"q0": {"a": "q0", "b": "q1"},
             "q1": {"a": "q0", "b": "q2"},
             "q2": {"a": "q3", "b": "q4"},
             "q3": {"a": "q3", "b": "q4"},
             "q4": {"a": "q3", "b": "q5"}}
        )

        assert dfa.levels_to_accepting_states() == \
               {
                   "q0": 3,
                   "q1": 2,
                   "q2": 1,
                   "q3": 0,
                   "q4": 1,
                   "q5": -1
               }


class TestToDot:

    def test_to_dot(self):

        dfa = DFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            {"a", "b"},
            "q0",
            {"q0"},
            {}
        )

        dfa.to_dot("./tmp/dfa", title="test dfa (initial state final)")

        dfa = DFA(
            {"q0", "q1", "q2", "q3", "q4", "q5"},
            {"a", "b"},
            "q0",
            {"q3"},
            {"q0": {"a": "q0", "b": "q1"},
             "q1": {"a": "q0", "b": "q2"},
             "q2": {"a": "q3", "b": "q4"},
             "q3": {"a": "q3", "b": "q4"},
             "q4": {"a": "q3", "b": "q5"}}
        )

        dfa.to_dot("./tmp/dfa", title="test dfa")

