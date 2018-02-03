#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pytest configuration."""

from sys import platform
import socket
import shutil
from selenium import webdriver

import pytest

from bowtie import View
from bowtie._app import _DIRECTORY


@pytest.fixture
def build_path():
    """Path for building apps with pytest."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 9991))
    if result == 0:
        raise Exception('Port 9991 is unavailable, aborting test.')
    # pylint: disable=protected-access
    View._NEXT_UUID = 0
    yield _DIRECTORY
    shutil.rmtree(_DIRECTORY)


@pytest.fixture
def chrome_driver():
    """Set up chrome driver."""
    options = webdriver.ChromeOptions()
    if platform == 'darwin':
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    else:
        options.binary_location = '/usr/bin/google-chrome-stable'
    options.add_argument('headless')
    options.add_argument('window-size=1200x800')
    driver = webdriver.Chrome(chrome_options=options)
    yield driver
    driver.quit()
