#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

import pytest
import selenium

from bowtie import Layout
from bowtie.control import Nouislider
from bowtie.visual import Plotly


@pytest.fixture
def remove_build(request):
    yield
    # shutil.rmtree('build')


def callback(*args):
    pass


def test_plotly(remove_build):
    ctrl = Nouislider()
    viz = Plotly()

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
    print(path)
    layout = Layout(directory=path)
    layout.add_controller(ctrl)
    layout.add_visual(viz)
    layout.subscribe(ctrl.on_change, callback)
    layout.build()

    rv = subprocess.Popen(os.path.join(path, 'src/server.py'))

    import IPython
    IPython.embed()

    ret = selenium.get('localhost:9991')
    print(ret)

    rv.kill()
