#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pytest configuration."""

import os
from subprocess import call
from sys import platform
import shutil
from selenium import webdriver

import pytest


@pytest.fixture
def remove_build():
    """Remove build directory after use."""
    yield
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
    shutil.rmtree(path)


@pytest.fixture
def chrome_driver():
    """Set up chrome driver."""
    options = webdriver.ChromeOptions()
    print('which chrome')
    print(call(['which', 'google-chrome-stable']))
    print(call(['ls', 'google*']))
    if platform == 'darwin':
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    else:
        options.binary_location = 'google-chrome-stable'
    options.add_argument('headless')
    options.add_argument('window-size=1200x800')
    return webdriver.Chrome(chrome_options=options)
