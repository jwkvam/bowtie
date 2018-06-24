"""Test layout functionality."""
# pylint: disable=redefined-outer-name,protected-access

import pytest

from bowtie import App
from bowtie.control import Button
from bowtie._app import GridIndexError, UsedCellsError, NoUnusedCellsError


@pytest.fixture(scope='module')
def buttons():
    """Four buttons."""
    return [Button() for _ in range(4)]


def app():
    """Simple app."""
    return App(rows=2, columns=2)


def test_all_used(buttons):
    """Test all cells are used."""

    app = App(rows=2, columns=2)
    for i in range(4):
        app.add(buttons[i])

    assert list(app._root._used.values()) == 4 * [True]

    app = App(rows=2, columns=2)
    app[0, 0] = buttons[0]
    app[0, 1] = buttons[1]
    app[1, 0] = buttons[2]
    app[1, 1] = buttons[3]

    assert list(app._root._used.values()) == 4 * [True]

    with pytest.raises(NoUnusedCellsError):
        app.add(buttons[2])

    app = App(rows=2, columns=2)
    app[0] = buttons[0]
    app[1, 0] = buttons[2]
    app[1, 1] = buttons[3]

    assert list(app._root._used.values()) == 4 * [True]

    with pytest.raises(NoUnusedCellsError):
        app.add(buttons[2])


def test_used(buttons):
    """Test cell usage checks."""

    app = App(rows=2, columns=2)
    for i in range(3):
        app.add(buttons[i])

    with pytest.raises(UsedCellsError):
        app[0, 0] = buttons[3]

    with pytest.raises(UsedCellsError):
        app[0:1, 1] = buttons[3]

    with pytest.raises(UsedCellsError):
        app[1, 0:1] = buttons[3]

    app[1, 1] = buttons[3]


def test_grid_index(buttons):
    """Test grid indexing checks."""

    app = App(rows=2, columns=2)
    with pytest.raises(GridIndexError):
        app[-5] = buttons[0]

    app[-1] = buttons[0]

    with pytest.raises(GridIndexError):
        app[2] = buttons[0]

    with pytest.raises(UsedCellsError):
        app[1] = buttons[0]


def test_getitem(buttons):
    """Test grid indexing checks."""

    but = buttons[0]

    app = App(rows=2, columns=2)

    with pytest.raises(GridIndexError):
        app[3] = but

    with pytest.raises(GridIndexError):
        app[1, 2, 3] = but

    with pytest.raises(GridIndexError):
        # pylint: disable=invalid-slice-index
        app['a':3] = but

    with pytest.raises(GridIndexError):
        app['a'] = but

    with pytest.raises(GridIndexError):
        app[3, 'a'] = but

    with pytest.raises(GridIndexError):
        app['a', 3] = but

    with pytest.raises(GridIndexError):
        app[0, 0::2] = but

    with pytest.raises(GridIndexError):
        app[0, 1:-1:-1] = but

    app[1, ] = but
    assert sum(app._root._used.values()) == 2
    app[0, :] = but
    assert sum(app._root._used.values()) == 4

    app = App(rows=2, columns=2)
    app[0:1, 1:2] = but
    assert sum(app._root._used.values()) == 1
    app[1:, 0:] = but
    assert sum(app._root._used.values()) == 3

    app = App(rows=2, columns=2)
    app[-1, :2] = but
    assert sum(app._root._used.values()) == 2

    app = App(rows=1, columns=2)
    app[0, :2] = but
    assert sum(app._root._used.values()) == 2

    app = App(rows=1, columns=2)
    app[0] = but
    assert sum(app._root._used.values()) == 2

    app = App(rows=2, columns=2)
    app[:2] = but
    assert sum(app._root._used.values()) == 4
