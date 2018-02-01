# -*- coding: utf-8 -*-
"""Test layout functionality."""
# pylint: disable=redefined-outer-name

import pytest

from bowtie import App
from bowtie.control import Button
from bowtie._app import MissingRowOrColumn, GridIndexError, UsedCellsError


@pytest.fixture(scope='module')
def buttons():
    """Four buttons."""
    return [Button() for _ in range(4)]


def test_no_row(buttons):
    """Test missing row."""

    app = App(rows=2, columns=3)
    with pytest.raises(MissingRowOrColumn):
        app.add(buttons[0], column_start=0, column_end=2)

    with pytest.raises(MissingRowOrColumn):
        app.add(buttons[0], column_start=0)


def test_no_column(buttons):
    """Test missing column."""

    app = App(rows=2, columns=3)
    with pytest.raises(MissingRowOrColumn):
        app.add(buttons[0], row_start=0, row_end=1)

    with pytest.raises(MissingRowOrColumn):
        app.add(buttons[0], row_start=0)


def test_all_used(buttons):
    """Test all cells are used."""

    app = App(rows=2, columns=2)
    for i in range(4):
        app.add(buttons[i])

    assert list(app.root.used.values()) == 4 * [True]


def test_used(buttons):
    """Test cell usage checks."""

    app = App(rows=2, columns=2)
    for i in range(3):
        app.add(buttons[i])

    with pytest.raises(UsedCellsError):
        app.add(buttons[3], row_start=0, column_start=0)

    with pytest.raises(UsedCellsError):
        app.add(buttons[3], row_start=0, column_start=1, row_end=1)

    with pytest.raises(UsedCellsError):
        app.add(buttons[3], row_start=1, column_start=0, column_end=1)

    app.add(buttons[3], row_start=1, column_start=1)


def test_grid_index(buttons):
    """Test grid indexing checks."""

    app = App(rows=2, columns=2)
    with pytest.raises(GridIndexError):
        app.add(buttons[0], row_start=-1)

    with pytest.raises(GridIndexError):
        app.add(buttons[0], row_start=2)
