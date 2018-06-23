#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,invalid-name
"""Multiple views testing."""

import os
from os import environ as env
import subprocess
import time

from numpy import random as rng
import pandas as pd
import pytest

from bowtie import App, View
from bowtie.control import Nouislider, Button
from bowtie.visual import Table
from bowtie.tests.utils import reset_uuid


reset_uuid()


table = Table()
ctrl = Nouislider()
ctrl2 = Button()


def callback(*args):
    """dummy function"""
    df = pd.DataFrame(rng.randn(10, 10))
    table.do_data(df)


@pytest.fixture
def multiple_views(build_path, monkeypatch):
    """Create multiple views app."""
    monkeypatch.setattr(App, '_sourcefile', lambda self: 'bowtie.tests.test_multiple')

    app = App()
    view1 = View()  # pylint: disable=unused-variable
    assert view1._uuid == 2  # pylint: disable=protected-access
    view2 = View()
    view2.add(table)
    app.add_route(view2, 'view2')

    app.add(table)
    app.add_sidebar(ctrl)
    app.add_sidebar(ctrl2)
    app.subscribe(callback, ctrl.on_change)
    app.subscribe(callback, ctrl2.on_click)

    app._build()  # pylint: disable=protected-access

    env['PYTHONPATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('PYTHONPATH', ''))
    server = subprocess.Popen(os.path.join(build_path, 'src/server.py'), env=env)

    time.sleep(5)
    yield
    server.kill()


# pylint: disable=redefined-outer-name,unused-argument
def test_multiple(multiple_views, chrome_driver):
    """Test multiple views app."""
    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    assert chrome_driver.title == 'Bowtie App'

    button = chrome_driver.find_element_by_class_name('ant-btn')
    data = chrome_driver.find_element_by_class_name('ant-table-body').text
    assert len(data.split('\n')) == 1
    button.click()
    time.sleep(2)

    data = chrome_driver.find_element_by_class_name('ant-table-body').text
    assert len(data.split('\n')) == 11

    logs = chrome_driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            raise Exception(log['message'])

    chrome_driver.get('http://localhost:9991/view2')
    data = chrome_driver.find_element_by_class_name('ant-table-body').text

    assert len(data.split('\n')) == 11

    chrome_driver.implicitly_wait(5)

    logs = chrome_driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            raise Exception(log['message'])

    chrome_driver.get('http://localhost:9991/view1')
    assert chrome_driver.title == '404 Not Found'
