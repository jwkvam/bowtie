"""Test markdown and text widgets."""
# pylint: disable=redefined-outer-name,unused-argument,invalid-name

import time

import pytest
from bowtie import App
from bowtie.html import Markdown
from bowtie.control import Textbox
from bowtie.tests.utils import reset_uuid, server_check


reset_uuid()

mark = Markdown('''
# top
## middle

[link]('hello.html')
''')
side = Markdown('''
# sideheader
''')
text = Textbox(area=True)


def write(txt):
    """Update markdown text."""
    mark.do_text(txt)


@pytest.fixture
def markdown(build_reset, monkeypatch):
    """Create markdown and text widgets."""
    app = App(__name__, sidebar=True)
    app.add(mark)
    app.add_sidebar(side)
    app.add_sidebar(text)
    app.subscribe(text.on_change)(write)
    # pylint: disable=protected-access
    app._build()

    with server_check(app) as server:
        yield server


def test_markdown(markdown, chrome_driver):
    """Test markdown and text widgets."""
    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    assert chrome_driver.title == 'Bowtie App'

    txtctrl = chrome_driver.find_element_by_class_name('ant-input')
    output = chrome_driver.find_element_by_xpath(
        "//div[@style='grid-area: 1 / 2 / 2 / 3; position: relative;']"
    )

    assert 'top' in output.text
    assert 'middle' in output.text
    assert 'link' in output.text

    txtctrl.send_keys('apple')
    time.sleep(1)

    assert 'apple' in output.text

    txtctrl.send_keys('banana')
    time.sleep(1)

    assert 'apple' in output.text
    assert 'banana' in output.text
