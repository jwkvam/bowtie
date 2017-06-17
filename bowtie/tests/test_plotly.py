#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plotly testing."""

import os
from os import environ as env
import subprocess
import time

from plotly.graph_objs import Scatter
from plotly.graph_objs import Layout as PlotLayout

from bowtie import Layout
from bowtie.control import Nouislider, Button
from bowtie.visual import Plotly
from bowtie.tests.utils import reset_uuid


reset_uuid()

# pylint: disable=invalid-name
viz = Plotly()
ctrl = Nouislider()
ctrl2 = Button()


def callback(*args):
    """dummy function"""
    # pylint: disable=unused-argument
    chart = {
        "data": [
            Scatter(x=[1, 2, 3, 4], y=[4, 1, 3, 7])
        ],
        "layout": PlotLayout(
            title="hello world"
        )
    }
    viz.do_all(chart)


# pylint: disable=unused-argument
def test_plotly(chrome_driver, build_path):
    """Tests plotly."""

    layout = Layout(directory=build_path)
    layout.add(viz)
    layout.add_sidebar(ctrl)
    layout.add_sidebar(ctrl2)
    layout.subscribe(callback, ctrl.on_change)
    layout.subscribe(callback, ctrl2.on_click)
    layout.build()

    env['PYTHONPATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('PYTHONPATH', ''))
    server = subprocess.Popen(os.path.join(build_path, 'src/server.py'), env=env)

    time.sleep(5)

    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    assert chrome_driver.title == 'Bowtie App'

    button = chrome_driver.find_element_by_class_name('ant-btn')
    button.click()

    points = chrome_driver.find_elements_by_class_name('point')

    assert len(points) == 4

    server.kill()
