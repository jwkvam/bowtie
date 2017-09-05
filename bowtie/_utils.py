# -*- coding: utf-8 -*-
"""Utility functions."""

import inspect


def func_name():
    """Return name of calling function."""
    return inspect.stack()[1][3]
