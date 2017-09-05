#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compat testing."""

from bowtie._utils import func_name


def hello():
    """A function."""
    return func_name()


def test_function_names():
    """Test we get the correct function name."""
    assert hello() == 'hello'
