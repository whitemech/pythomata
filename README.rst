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

.. code-block:: console

    $ wget http://204.178.9.49/pub/graphviz/stable/ubuntu/ub13.10/x86_64/graphviz_2.38.0-1~saucy_amd64.deb
    $ sudo dpkg -i graphviz_2.38.0-1~saucy_amd64.deb
    $ sudo apt-get install -f


Features
--------

* Basic DFA and NFA support;
* Algorithms for DFA minimization and trimming;
* Algorithm for NFA determinization.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
