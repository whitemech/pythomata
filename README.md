# Pythomata


[![](https://img.shields.io/pypi/v/pythomata.svg)](https://pypi.python.org/pypi/pythomata)
[![](https://img.shields.io/travis/marcofavorito/pythomata.svg)](https://travis-ci.org/marcofavorito/pythomata)
[![](https://img.shields.io/pypi/pyversions/pythomata.svg)](https://pypi.python.org/pypi/pythomata)
[![](https://readthedocs.org/projects/pythomata/badge/?version=latest)](https://pythomata.readthedocs.io/en/latest/?badge=latest)
[![](https://img.shields.io/badge/status-development-orange.svg)](https://img.shields.io/badge/status-development-orange.svg)
[![](https://coveralls.io/repos/github/marcofavorito/pythomata/badge.svg?branch=master)](https://coveralls.io/github/marcofavorito/pythomata?branch=master)
[![](https://img.shields.io/badge/flake8-checked-blueviolet)](https://img.shields.io/badge/flake8-checked-blueviolet)
[![](https://img.shields.io/badge/mypy-checked-blue)](https://img.shields.io/badge/mypy-checked-blue)
[![](https://img.shields.io/badge/license-Apache%202-lightgrey)](https://img.shields.io/badge/license-Apache%202-lightgrey)

Python implementation of automata theory.


* Free software: Apache 2.0
* Documentation: https://pythomata.readthedocs.io.

## Install

### Graphviz


For Debian systems, the following commands should work:

    $ wget http://ftp.it.debian.org/debian/pool/main/g/graphviz/graphviz_2.38.0-17_amd64.deb
    $ sudo dpkg -i graphviz_2.38.0-1~saucy_amd64.deb
    $ sudo apt-get install -f

Otherwise check the installation guide from the [official site](https://www.graphviz.org/download/).

## How to use

* Define an automaton:


    from pythomata.dfa import DFA
    alphabet = {"a", "b", "c"}
    states = {"s1", "s2", "s3"}
    initial_state = "s1"
    accepting_states = {"s3"}
    transition_function = {
        "s1": {
            "b" : "s1",
            "a" : "s2"
        },
        "s2": {
            "a" : "s3",
            "b" : "s1"
        },
        "s3":{
            "c" : "s3"
        }
    }
    dfa = DFA(states, alphabet, initial_state, accepting_states, transition_function)  


* Test word acceptance:


    # a word is a list of symbols
    word = [b, b, b, a, b, c]

    dfa.accepts(word)        # True

    # without the last symbol c, the final state is not reached
    dfa.accepts(word[:-1])   # False

* Operations such as minimization and trimming:


    dfa_minimized = dfa.minimize()
    dfa_trimmed = dfa.trim()

* Print the automata:


    filepath = "./my_awesome_automaton"
    dfa.minimize().trim().to_dot(filepath)

The output in .svg format is the following:

![](https://github.com/marcofavorito/pythomata/tree/master/docs/my_awesome_automaton.svg)


## Features


* Basic DFA and NFA support;
* Algorithms for DFA minimization and trimming;
* Algorithm for NFA determinization;
* Print automata in SVG format.
