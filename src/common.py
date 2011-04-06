# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Utility functions used by both the client and server code."""

import sys

def impossible(text):
    """Abort with an error message."""
    sys.stderr.write('Impossible area of code reached\n' + text)
    exit(0)


def flatten_args(x, y):
    """If x is a tuple, put its two values into x and y."""
    if isinstance(x, tuple):
        return x[0], x[1]
    else:
        return x, y
