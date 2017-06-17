#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compile tests."""

from bowtie import Layout
from bowtie.control import Nouislider
from bowtie.visual import Plotly
from bowtie.tests.utils import reset_uuid


def callback(*args):
    """dummy function"""
    # pylint: disable=unused-argument
    pass


# pylint: disable=unused-argument
def test_build(build_path):
    """Tests the build process."""
    reset_uuid()
    ctrl = Nouislider()
    viz = Plotly()

    layout = Layout(directory=build_path)
    layout.add_sidebar(ctrl)
    layout.add(viz)
    layout.subscribe(callback, ctrl.on_change)
    layout.build()
