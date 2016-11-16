#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

import pytest

from bowtie import Layout
from bowtie.control import Nouislider
from bowtie.visual import Plotly


@pytest.fixture
def remove_build(request):
    yield
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
    shutil.rmtree(path)


def callback(*args):
    pass


def test_build(remove_build):
    ctrl = Nouislider()
    viz = Plotly()

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
    layout = Layout(directory=path)
    layout.add_controller(ctrl)
    layout.add_visual(viz)
    layout.subscribe(ctrl.on_change, callback)
    layout.build()
