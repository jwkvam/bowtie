"""Multiple views testing."""
# pylint: disable=unused-argument,redefined-outer-name,invalid-name

from time import sleep

from numpy import random as rng
import pandas as pd
import pytest

from bowtie import App, View
from bowtie.control import Nouislider, Button
from bowtie.visual import Table
from bowtie.tests.utils import reset_uuid, server_check


reset_uuid()


table = Table()
ctrl = Nouislider()
ctrl2 = Button()


def callback(*args):
    """dummy function"""
    df = pd.DataFrame(rng.randn(10, 10))
    table.do_data(df)


@pytest.fixture
def multiple_views(build_reset, monkeypatch):
    """Create multiple views app."""
    app = App(__name__, sidebar=True)
    view1 = View()  # pylint: disable=unused-variable
    assert view1._uuid == 2  # pylint: disable=protected-access
    view2 = View()
    view2.add(table)
    app.add_route(view2, 'view2')

    app.add(table)
    app.add_sidebar(ctrl)
    app.add_sidebar(ctrl2)
    app.subscribe(ctrl.on_change)(app.subscribe(ctrl2.on_click)(callback))

    app._build()  # pylint: disable=protected-access

    with server_check(app) as server:
        yield server


# pylint: disable=redefined-outer-name,unused-argument
def test_multiple(multiple_views, chrome_driver):
    """Test multiple views app."""
    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    assert chrome_driver.title == 'Bowtie App'

    button = chrome_driver.find_element_by_class_name('ant-btn')
    data = chrome_driver.find_element_by_class_name('ant-table-body').text
    assert len(data.split('\n')) == 1
    button.click()
    sleep(2)

    data = chrome_driver.find_element_by_class_name('ant-table-body').text
    assert len(data.split('\n')) == 20

    logs = chrome_driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            raise Exception(log['message'])

    chrome_driver.get('http://localhost:9991/view2')
    data = chrome_driver.find_element_by_class_name('ant-table-body').text

    assert len(data.split('\n')) == 20

    chrome_driver.implicitly_wait(5)

    logs = chrome_driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            raise Exception(log['message'])

    chrome_driver.get('http://localhost:9991/view1')
    assert chrome_driver.title == '404 Not Found'
