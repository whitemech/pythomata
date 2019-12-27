# -*- coding: utf-8 -*-
from pythomata.v3.alphabets import MapAlphabet
from pythomata.v3.dfas import SimpleDFA


def test_simple_dfa():
    dfa = SimpleDFA(
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

    assert dfa.accepts(['a', 'b', 'c'])
    assert not dfa.accepts(['a', 'b', 'c', 'a'])
    assert dfa.accepts(['a', 'b', 'c', 'b', 'c'])
