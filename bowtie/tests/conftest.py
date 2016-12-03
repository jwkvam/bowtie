#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pytest configuration
"""

import os
import shutil

import pytest


@pytest.fixture
def remove_build():
    """
    Removes build directory after use.
    """
    yield
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
    shutil.rmtree(path)
