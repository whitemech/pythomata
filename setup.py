#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""
import os

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'pythomata', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    description=about['__description__'],
    version=about['__version__'],
    author=about['__author__'],
    url=about['__url__'],
    author_email=about["__author_email__"],
    long_description=readme + '\n\n' + history,
    packages=find_packages(include=['pythomata*']),
    include_package_data=True,
    install_requires=["graphviz"],
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
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
)
