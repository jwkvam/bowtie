#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compat testing."""

from bowtie._utils import func_name


def hello():
    return func_name()


def test_function_names():
    assert hello() == 'hello'
