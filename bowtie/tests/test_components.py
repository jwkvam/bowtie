#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test all components for instatiation issues."""

import os
from os import environ as env
import subprocess
import time

import pytest
from bowtie import App
from bowtie import control, visual
from bowtie._component import COMPONENT_REGISTRY
from bowtie.tests.utils import reset_uuid


def create_components():
    """Create components for this test."""
    reset_uuid()
    # pylint: disable=protected-access
    controllers = [getattr(control, comp)() for comp in dir(control)
                   if comp[0].isupper() and issubclass(getattr(control, comp),
                                                       control._Controller) and comp != 'Upload']
    for controller in controllers:
        assert COMPONENT_REGISTRY[controller._uuid] == controller

    visuals = [getattr(visual, comp)() for comp in dir(visual)
               if comp[0].isupper() and issubclass(getattr(visual, comp), visual._Visual)]
    for vis in visuals:
        assert COMPONENT_REGISTRY[vis._uuid] == vis

    return controllers, visuals


create_components()


@pytest.fixture
def components(build_path, monkeypatch):
    """App with all components."""
    monkeypatch.setattr(App, '_sourcefile', lambda self: 'bowtie.tests.test_components')

    controllers, visuals = create_components()

    app = App(rows=len(visuals))
    for controller in controllers:
        # pylint: disable=protected-access
        assert COMPONENT_REGISTRY[controller._uuid] == controller
        app.add_sidebar(controller)

    for vis in visuals:
        # pylint: disable=protected-access
        assert COMPONENT_REGISTRY[vis._uuid] == vis
        app.add(vis)

    # pylint: disable=protected-access
    app._build()

    env['PYTHONPATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('PYTHONPATH', ''))
    server = subprocess.Popen(os.path.join(build_path, 'src/server.py'), env=env)

    time.sleep(5)
    yield
    server.kill()


# pylint: disable=redefined-outer-name,unused-argument
def test_components(components, chrome_driver):
    """Test that no components cause an error."""
    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    logs = chrome_driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            raise Exception(log['message'])
