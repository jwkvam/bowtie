#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil

import pytest

from bowtie import Layout
from bowtie.control import Nouislider
from bowtie.visual import Plotly


@pytest.fixture
def remove_build(request):
    import os
    print(os.getcwd())
    yield
    shutil.rmtree('build')


def callback(*args):
    pass


def test_build(remove_build):
    ctrl = Nouislider()
    viz = Plotly()

    layout = Layout()
    layout.add_controller(ctrl)
    layout.add_visual(viz)
    layout.subscribe(ctrl.on_change, callback)
    layout.build()
