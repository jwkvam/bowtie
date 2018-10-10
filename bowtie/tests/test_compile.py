#!/usr/bin/env python
"""Compile tests."""

from bowtie import App
from bowtie.control import Nouislider
from bowtie.visual import Plotly
from bowtie.tests.utils import reset_uuid


def callback(*args):
    """dummy function"""
    # pylint: disable=unused-argument
    pass


# pylint: disable=unused-argument
def test_build(build_reset, monkeypatch):
    """Tests the build process."""
    reset_uuid()
    ctrl = Nouislider()
    viz = Plotly()

    app = App(__name__, sidebar=True)
    app.add_sidebar(ctrl)
    app.add(viz)
    app.subscribe(ctrl.on_change)(callback)
    # pylint: disable=protected-access
    app._build()
