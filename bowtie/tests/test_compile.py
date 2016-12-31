#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile tests
"""

import os

from bowtie import Layout
from bowtie.control import Nouislider
from bowtie.visual import Plotly


def callback(*args):
    """dummy function"""
    # pylint: disable=unused-argument
    pass


# pylint: disable=unused-argument
def test_build(remove_build):
    """
    Tests the build process.
    """
    ctrl = Nouislider()
    viz = Plotly()

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
    layout = Layout(directory=path)
    layout.add_controller(ctrl)
    layout.add_visual(viz)
    layout.subscribe(callback, ctrl.on_change)
    layout.build()
