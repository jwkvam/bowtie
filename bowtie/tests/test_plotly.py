#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plotly testing."""

import os
from os import environ as env
import subprocess
import time

from plotly.graph_objs import Scatter
from plotly.graph_objs import Layout as PlotLayout

from bowtie import App
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
        "app": PlotLayout(
            title="hello world"
        )
    }
    viz.do_all(chart)


# pylint: disable=unused-argument
def test_plotly(chrome_driver, build_path):
    """Tests plotly."""

    app = App(directory=build_path)
    app.add(viz)
    app.add_sidebar(ctrl)
    app.add_sidebar(ctrl2)
    app.subscribe(callback, ctrl.on_change)
    app.subscribe(callback, ctrl2.on_click)
    app.build()

    env['PYTHONPATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('PYTHONPATH', ''))
    server = subprocess.Popen(os.path.join(build_path, 'src/server.py'), env=env)

    time.sleep(5)

    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    assert chrome_driver.title == 'Bowtie App'

    button = chrome_driver.find_element_by_class_name('ant-btn')
    button.click()

    points = chrome_driver.find_elements_by_class_name('point')

    logs = chrome_driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            raise Exception(log['message'])

    assert len(points) == 4

    server.kill()
