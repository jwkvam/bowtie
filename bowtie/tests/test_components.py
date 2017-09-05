#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test all components for instatiation issues."""

import os
from os import environ as env
import subprocess
import time

from bowtie import Layout
from bowtie import control, visual
from bowtie.tests.utils import reset_uuid

reset_uuid()

# pylint: disable=invalid-name,protected-access
controllers = [getattr(control, comp)() for comp in dir(control)
               if comp[0].isupper() and issubclass(getattr(control, comp), control._Controller) and
               comp != 'Upload']

visuals = [getattr(visual, comp)() for comp in dir(visual)
           if comp[0].isupper() and issubclass(getattr(visual, comp), visual._Visual)]


# pylint: disable=unused-argument
def test_components(chrome_driver, build_path):
    """Tests plotly."""

    layout = Layout(rows=len(visuals), directory=build_path)
    for controller in controllers:
        layout.add_sidebar(controller)

    for vis in visuals:
        layout.add(vis)
    layout.build()

    env['PYTHONPATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('PYTHONPATH', ''))
    server = subprocess.Popen(os.path.join(build_path, 'src/server.py'), env=env)

    time.sleep(5)

    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    logs = chrome_driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            raise Exception(log['message'])

    server.kill()
