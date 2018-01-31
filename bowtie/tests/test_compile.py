#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
def test_build(build_path, monkeypatch):
    """Tests the build process."""
    monkeypatch.setattr(App, '_sourcefile', lambda self: 'bowtie.tests.test_compile')
    reset_uuid()
    ctrl = Nouislider()
    viz = Plotly()

    app = App()
    app.add_sidebar(ctrl)
    app.add(viz)
    app.subscribe(callback, ctrl.on_change)
    # pylint: disable=protected-access
    app._build()
