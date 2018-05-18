# -*- coding: utf-8 -*-
"""Utility functions for testing only."""

import os
from os.path import join as pjoin
from os import environ as env
from contextlib import contextmanager
from subprocess import Popen, PIPE
import time

from bowtie import View
from bowtie._component import Component


def reset_uuid():
    """Reset the uuid counter for components."""
    # pylint: disable=protected-access
    Component._NEXT_UUID = 0
    View._NEXT_UUID = 0


@contextmanager
def server_check(build_path):
    """Context manager for testing Bowtie apps and verifying no errors happened."""
    env['PYTHONPATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('PYTHONPATH', ''))
    server = Popen(['python', '-u', pjoin(build_path, 'src/server.py')], env=env, stderr=PIPE)
    time.sleep(5)
    yield server
    server.terminate()
    _, stderr = server.communicate()
    assert b'Error' not in stderr
    assert b'Traceback' not in stderr
