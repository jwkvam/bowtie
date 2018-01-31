# -*- coding: utf-8 -*-
"""Test markdown and text widgets."""

import os
from os import environ as env
import subprocess
import time

from bowtie import App
from bowtie.visual import Markdown
from bowtie.control import Textbox
from bowtie.tests.utils import reset_uuid


reset_uuid()

# pylint: disable=invalid-name
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


# pylint: disable=unused-argument
def test_markdown(chrome_driver, build_path, monkeypatch):
    """Test markdown and text widgets."""
    monkeypatch.setattr(App, '_sourcefile', lambda self: 'bowtie.tests.test_editor')

    app = App()
    app.add(mark)
    app.add_sidebar(side)
    app.add_sidebar(text)
    app.subscribe(write, text.on_change)
    # pylint: disable=protected-access
    app._build()

    env['PYTHONPATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('PYTHONPATH', ''))
    server = subprocess.Popen(os.path.join(build_path, 'src/server.py'), env=env)

    time.sleep(5)

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

    server.kill()
