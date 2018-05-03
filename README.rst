=========
Pythomata
=========


.. image:: https://img.shields.io/pypi/v/pythomata.svg
        :target: https://pypi.python.org/pypi/pythomata

.. image:: https://img.shields.io/pypi/pyversions/pythomata.svg
        :target: https://pypi.python.org/pypi/pythomata

.. image:: https://img.shields.io/badge/status-development-orange.svg
        :target: https://img.shields.io/badge/status-development-orange.svg

.. image:: https://img.shields.io/travis/MarcoFavorito/pythomata.svg
        :target: https://travis-ci.org/MarcoFavorito/pythomata

.. image:: https://readthedocs.org/projects/pythomata/badge/?version=latest
        :target: https://pythomata.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/MarcoFavorito/pythomata/branch/master/graph/badge.svg
        :alt: Codecov coverage
        :target: https://codecov.io/gh/MarcoFavorito/pythomata/branch/master/graph/badge.svg


Python implementation of automata.


* Free software: MIT license
* Documentation: https://pythomata.readthedocs.io.

Install
-------

Graphviz
~~~~~~~~~~~~~~~~~~~~~~

For Debian systems, the following commands should work:

.. code-block:: console

    $ wget http://ftp.it.debian.org/debian/pool/main/g/graphviz/graphviz_2.38.0-17_amd64.deb
    $ sudo dpkg -i graphviz_2.38.0-1~saucy_amd64.deb
    $ sudo apt-get install -f

Otherwise check the installation guide from the `official site <https://www.graphviz.org/download/>`_

How to use
--------

* Define an automaton:

.. code-block:: python

    a, b, c = Symbol("a"), Symbol("b"), Symbol("c")
        alphabet = Alphabet({a, b, c})
        states = frozenset({"s1", "s2", "s3"})
        initial_state = "s1"
        accepting_states = frozenset({"s3"})
        transition_function = {
            "s1": {
                b : "s1",
                a : "s2"
            },
            "s2": {
                a : "s3",
                b : "s1"
            },
            "s3":{
                c : "s3"
            }
        }

        dfa = DFA(alphabet, states, initial_state, accepting_states, transition_function)

* Test word acceptance:

.. code-block:: python

    # a word is a list of symbols
    word = [b, b, b, a, b, c]

    dfa.word_acceptance(word)        # True

    # without the last symbol c, the final state is not reached
    dfa.word_acceptance(word[:-1])   # False

* Operations such as minimization and trimming:

.. code-block:: python


    dfa_minimized = dfa.minimize()
    dfa_trimmed = dfa.trim()

* Print the automata:

.. code-block:: python

    filepath = "./my_awesome_automaton"
    dfa.minimize().trim().to_dot(filepath)

The output in .svg format is the following:

.. image:: https://github.com/MarcoFavorito/pythomata/tree/master/docs/my_awesome_automaton.svg


Features
--------

* Basic DFA and NFA support;
* Algorithms for DFA minimization and trimming;
* Algorithm for NFA determinization;
* Print automata in SVG format.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
