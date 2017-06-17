#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pytest configuration."""

import os
from sys import platform
import shutil
from selenium import webdriver

import pytest


@pytest.fixture
def build_path():
    """Path for building apps with pytest."""
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
    yield path
    shutil.rmtree(path)


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
