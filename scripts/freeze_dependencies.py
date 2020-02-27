#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This CLI tool freezes the dependencies of the caller interpreter.
"""
import re
import subprocess
import sys


def parse_args():
    """Parse CLI arguments."""
    import argparse

    parser = argparse.ArgumentParser("freeze_dependencies")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default=None)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()

    pip_freeze_call = subprocess.Popen(
        [sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE
    )
    (stdout, stderr) = pip_freeze_call.communicate()
    requirements = stdout.decode("utf-8")

    # remove 'pythomata' itself
    requirements = re.sub("pythomata==.*\n", "", requirements)
    if arguments.output is None:
        print(requirements)
    else:
        arguments.output.write(requirements)
