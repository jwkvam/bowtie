# -*- coding: utf-8 -*-
"""Test markdown and text widgets."""

import time

import pytest
from bowtie import App, cache
from bowtie.control import Button
from bowtie.tests.utils import reset_uuid, server_check


reset_uuid()


# pylint: disable=invalid-name
button = Button()


def click():
    """Update markdown text."""
    cache['a'] = 3
    assert cache[b'a'] == 3
    assert cache[u'a'] == 3
    cache[b'b'] = True
    assert cache[b'b']
    assert cache[u'b']


def test_keys():
    """Test invalid keys."""
    with pytest.raises(KeyError):
        cache[0] = 0

    with pytest.raises(KeyError):
        cache[True] = 0

    with pytest.raises(KeyError):
        cache[3, 4] = 0


@pytest.fixture
def dummy(build_path, monkeypatch):
    """Create markdown and text widgets."""
    monkeypatch.setattr(App, '_sourcefile', lambda self: 'bowtie.tests.test_cache')

    app = App()
    app.add(button)
    app.subscribe(click, button.on_click)
    # pylint: disable=protected-access
    app._build()

    with server_check(build_path) as server:
        yield server


# pylint: disable=redefined-outer-name,unused-argument
def test_cache(dummy, chrome_driver):
    """Test markdown and text widgets."""
    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    assert chrome_driver.title == 'Bowtie App'

    btx = chrome_driver.find_element_by_class_name('ant-btn')
    btx.click()
    time.sleep(2)
