#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

import pytest
from selenium.webdriver import PhantomJS, ActionChains

from bowtie import Layout
from bowtie.control import Nouislider
from bowtie.visual import Plotly


@pytest.fixture
def remove_build(request):
    yield
    shutil.rmtree('build')


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

    driver = PhantomJS()
    driver.get('http://localhost:9991')

    assert driver.title == 'Bowtie App'

    rv.kill()
