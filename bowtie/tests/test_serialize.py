#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Serialization testing."""

import numpy as np
import pandas as pd

from bowtie._component import jdumps, pack


NPARRAY = np.array([5, 6])
NPSCALAR = np.int32(5)
DATES = pd.date_range('2017-01-01', periods=2)


def test_json():
    """Tests json encoding numpy and pandas."""
    assert jdumps(NPARRAY) == jdumps([5, 6])
    assert jdumps(NPSCALAR) == jdumps(5)
    assert jdumps(DATES) == jdumps(['2017-01-01T00:00:00', '2017-01-02T00:00:00'])


def test_msgpack():
    """Tests msgpack encoding numpy and pandas."""
    assert pack(NPARRAY) == pack([5, 6])
    assert pack(NPSCALAR) == pack(5)
    assert pack(DATES) == pack(['2017-01-01T00:00:00', '2017-01-02T00:00:00'])
