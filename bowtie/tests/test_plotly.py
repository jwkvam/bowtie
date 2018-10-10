"""Plotly testing."""
# pylint: disable=redefined-outer-name,unused-argument,invalid-name

import pytest
from plotly import graph_objs as go

from bowtie import App
from bowtie.control import Nouislider, Button
from bowtie.visual import Plotly
from bowtie.tests.utils import reset_uuid, server_check


reset_uuid()

viz = Plotly()
ctrl = Nouislider()
ctrl_range = Nouislider(start=(20, 200))
ctrl2 = Button()


def callback(*args):
    """dummy function"""
    chart = go.Figure()
    chart.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[4, 1, 3, 7]))
    chart.layout.title = 'hello world'
    viz.do_all(chart.to_dict())


@pytest.fixture
def plotly(build_reset, monkeypatch):
    """Create plotly app."""
    app = App(__name__, sidebar=True)
    app.add(viz)
    app.add_sidebar(ctrl)
    app.add_sidebar(ctrl_range)
    app.add_sidebar(ctrl2)
    app.subscribe(ctrl.on_change)(app.subscribe(ctrl2.on_click)(callback))
    # pylint: disable=protected-access
    app._build()

    with server_check(app) as server:
        yield server


def test_plotly(plotly, chrome_driver):
    """Test plotly component."""
    chrome_driver.get('http://localhost:9991')
    chrome_driver.implicitly_wait(5)

    assert chrome_driver.title == 'Bowtie App'

    button = chrome_driver.find_element_by_class_name('ant-btn')
    points = chrome_driver.find_elements_by_class_name('point')
    assert not points

    button.click()

    points = chrome_driver.find_elements_by_class_name('point')

    logs = chrome_driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            raise Exception(log['message'])

    assert len(points) == 4
