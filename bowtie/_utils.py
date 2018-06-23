"""Utility functions."""

import inspect


def func_name() -> str:
    """Return name of calling function."""
    return inspect.stack()[1].function
