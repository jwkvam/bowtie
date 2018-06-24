#!/usr/bin/env python
"""Test all components for instatiation issues."""

import os
from os import environ as env
import subprocess
from inspect import isclass
import time

import pytest
from bowtie import App
from bowtie import control, visual, html
from bowtie._component import COMPONENT_REGISTRY
from bowtie.tests.utils import reset_uuid


def create_components():
    """Create components for this test."""
    reset_uuid()
    # pylint: disable=protected-access
    controllers = []
    for compstr in dir(control):
        comp = getattr(control, compstr)
        if (compstr[0] != '_' and isclass(comp) and issubclass(comp, control._Controller)
                and compstr != 'Upload'):
            controllers.append(comp())

    for controller in controllers:
        assert COMPONENT_REGISTRY[controller._uuid] == controller

    visuals = []
    for compstr in dir(visual):
        comp = getattr(visual, compstr)
        if compstr[0] != '_' and isclass(comp) and issubclass(comp, visual._Visual):
            visuals.append(comp())

    for vis in visuals:
        assert COMPONENT_REGISTRY[vis._uuid] == vis

    htmls = []
    for compstr in dir(html):
        comp = getattr(html, compstr)
        if compstr[0] != '_' and isclass(comp) and issubclass(comp, html._HTML):
            htmls.append(comp())

    for htm in htmls:
        assert COMPONENT_REGISTRY[htm._uuid] == htm

    return controllers, visuals, htmls


create_components()


@pytest.fixture
def components(build_path, monkeypatch):
    """App with all components."""
    monkeypatch.setattr(App, '_sourcefile', lambda self: 'bowtie.tests.test_components')

    controllers, visuals, htmls = create_components()

    app = App(rows=len(visuals))
    for controller in controllers:
        # pylint: disable=protected-access
        assert COMPONENT_REGISTRY[controller._uuid] == controller
        app.add_sidebar(controller)

    for vis in visuals:
        # pylint: disable=protected-access
        assert COMPONENT_REGISTRY[vis._uuid] == vis
        app.add(vis)

    for htm in htmls:
        # pylint: disable=protected-access
        assert COMPONENT_REGISTRY[htm._uuid] == htm
        app.add_sidebar(htm)

    assert len(COMPONENT_REGISTRY) == len(controllers) + 2 * len(visuals) + len(htmls)

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
