#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compat testing."""

from bowtie._compat import numargs


def test_numargs():
    """Numargs testing."""

    # pylint: disable=missing-docstring
    def onearg(x):
        return x

    def zeroarg():
        pass

    def varargs(*y):
        return y

    def onevarargs(x, *y):
        return x, y

    assert numargs(onearg) == 1
    assert numargs(onevarargs) == 2
    assert numargs(zeroarg) == 0
    assert numargs(varargs) == 1
