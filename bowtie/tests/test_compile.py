#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compile tests."""

from bowtie import App
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

    app = App(directory=build_path)
    app.add_sidebar(ctrl)
    app.add(viz)
    app.subscribe(callback, ctrl.on_change)
    app.build()
