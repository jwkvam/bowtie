# -*- coding: utf-8 -*-
"""Utility functions."""

import inspect


def func_name():
    return inspect.stack()[1][3]
