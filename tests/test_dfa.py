import pytest

from pythomata.dfa import DFA


class TestDFA:
    """Basic tests for the DFA class."""

    def test_instantiate_dfa(self):
        """Test that we can instantiate a simple DFA."""
        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a0", "a1"},
            "q0",
            {"q2"},
            {("q0", "a0"): "q1", ("q1", "a1"): "q2"}
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


class TestCheckConsistency:
    """Test suite to check the input is validated as expected."""

    def test_empty_set_of_states_raise_error(self):
        """Test that when we try to instantiate a DFA with an empty set of states we raise an error."""
        with pytest.raises(ValueError, match="The set of states cannot be empty."):
            dfa = DFA(set(), {"a"}, "q0", set(), {})


class TestIsComplete:

    def test_is_complete_when_dfa_is_complete(self):
        """Test that the is_complete method return True if the DFA is complete."""
        dfa = DFA(
            {"q"},
            {"a"},
            "q",
            set(),
            {("q", "a"): "q"}
        )
        assert dfa.is_complete()


class TestComplete:

    def test_complete_when_dfa_is_already_complete(self):
        """Test that when we try to make complete an already complete DFA
        then the returned DFA is equal to the previous one."""

        complete_dfa = DFA(
            {"q"},
            {"a"},
            "q",
            set(),
            {("q", "a"): "q"}
        )

        new_dfa = complete_dfa.complete()
        assert complete_dfa == new_dfa


class TestMinimize:

    def test_minimize(self):

        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a1"},
            "q0",
            {"q1", "q2"},
            {("q0", "a1"): "q1", ("q1", "a1"): "q2", ("q2", "a1"): "q2"}
        )

        minimized = dfa.minimize()


class TestReachable:

    def test_reachable(self):

        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a1", "a2"},
            "q0",
            {"q0"},
            {("q0", "a1"): "q0", ("q0", "a2"): "q1"}
        )

        actual_reachable = dfa.reachable()

        expected_reachable = DFA(
            {"q0", "q1"},
            {"a1", "a2"},
            "q0",
            {"q0"},
            {("q0", "a1"): "q0", ("q0", "a2"): "q1"}
        )

        assert actual_reachable == expected_reachable


class TestCoReachable:

    def test_coreachable(self):

        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a1", "a2"},
            "q0",
            {"q0"},
            {("q0", "a1"): "q0", ("q0", "a2"): "q1"}
        )

        actual_coreachable = dfa.coreachable()

        expected_coreachable = DFA(
            {"q0"},
            {"a1", "a2"},
            "q0",
            {"q0"},
            {("q0", "a1"): "q0"}
        )

        assert actual_coreachable == expected_coreachable
