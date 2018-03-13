#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pythomata` package."""


import unittest
from click.testing import CliRunner

from pythomata import pythomata
from pythomata import cli


class TestPythomata(unittest.TestCase):
    """Tests for `pythomata` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'pythomata.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
