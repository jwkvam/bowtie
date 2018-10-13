"""Test markdown and text widgets."""
# pylint: disable=unused-argument,redefined-outer-name,invalid-name

import time

import pytest
from bowtie import App, cache
from bowtie.control import Button
from bowtie.tests.utils import reset_uuid, server_check


reset_uuid()


button = Button()


def click():
    """Save and load cache."""
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
def dummy(build_reset, monkeypatch):
    """Create basic app."""
    app = App(__name__)
    app.add(button)
    app.subscribe(button.on_click)(click)
    app._build()  # pylint: disable=protected-access

    with server_check(app) as server:
        yield server


def test_cache(dummy, chrome_driver):
    """Test cache works."""
    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    assert chrome_driver.title == 'Bowtie App'

    btx = chrome_driver.find_element_by_class_name('ant-btn')
    btx.click()
    time.sleep(2)
