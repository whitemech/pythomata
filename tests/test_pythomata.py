#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pythomata` package."""


import unittest

from pythomata.base.Alphabet import Alphabet
from pythomata.base.DFA import DFA
from pythomata.base.Symbol import Symbol


class TestPythomata(unittest.TestCase):
    """Tests for `pythomata` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_readme_example(self):
        a, b, c = Symbol("a"), Symbol("b"), Symbol("c")
        alphabet = Alphabet({a, b, c})
        states = frozenset({"s1", "s2", "s3"})
        initial_state = "s1"
        accepting_states = frozenset({"s3"})

        transition_function = {
            "s1": {
                b: "s1",
                a: "s2"
            },
            "s2": {
                c: "s3",
                b: "s1",
                a: "s1"
            },
            "s3":{
                c: "s3"
            }
        }

        dfa = DFA(alphabet, states, initial_state, accepting_states, transition_function)

        word = [b, b, b, a, b, a, c]
        self.assertTrue(dfa.word_acceptance(word))
        self.assertFalse(dfa.word_acceptance(word[:-1]))

        # dfa.minimize().to_dot("dfa_minimized_example")
        # dfa.trim().to_dot("dfa_trimmed_example")
        dfa.minimize().trim().to_dot("docs/my_awesome_automaton")


