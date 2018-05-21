#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["graphviz", "pydot", "pyparsing"]
# requirements = []

# setup_requirements = ["graphviz", "pydot", "pyparsing"]
setup_requirements = []

# test_requirements = ["graphviz", "pydot", "pyparsing"]
test_requirements = []

setup(
    name='pythomata',
    version='0.1.4post8',
    description="Python implementation of automata.",
    long_description=readme + '\n\n' + history,
    author="Marco Favorito",
    author_email='marco.favorito@gmail.com',
    url='https://github.com/MarcoFavorito/pythomata',
    packages=find_packages(include=['pythomata*']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pythomata',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    # setup_requires=setup_requirements,
    # tests_require=test_requirements,
)
