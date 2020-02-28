"""This module contains tests for alphabets."""

from pythomata import SimpleDFA


def test_even_01_automaton():
    """Test the even-01 automaton in the documentation."""

    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"0", "1"}
    initial_state = "q0"
    accepting_states = {"q0"}
    transition_function = {
        "q0": {"0": "q2", "1": "q1"},
        "q1": {"0": "q3", "1": "q0"},
        "q2": {"0": "q0", "1": "q3"},
        "q3": {"0": "q1", "1": "q2"},
    }
    automaton = SimpleDFA(
        states=states,
        alphabet=alphabet,
        initial_state=initial_state,
        accepting_states=accepting_states,
        transition_function=transition_function,
    )

    assert automaton.is_complete()

    assert automaton.accepts("")  # True
    assert not automaton.accepts("0")  # False - only one '0'
    assert not automaton.accepts("1")  # False - only one '1'
    assert automaton.accepts("00")  # True
    assert automaton.accepts("11")  # True
    assert automaton.accepts("01" * 42)  # True
