"""Test layout functionality."""
# pylint: disable=redefined-outer-name,protected-access

import pytest

from bowtie import App
from bowtie.control import Button
from bowtie.exceptions import GridIndexError, NoUnusedCellsError, SpanOverlapError


def check_all_cells_used(view):
    """Check if all cells are used."""
    with pytest.raises(NoUnusedCellsError):
        view._available_cell()


def count_used_cells(view):
    """Count number of used cells."""
    return sum(len(list(x.cells)) for x in view._spans.keys())


@pytest.fixture(scope='module')
def buttons():
    """Four buttons."""
    return [Button() for _ in range(4)]


def test_add_list(buttons):
    """Append button to existing cell."""
    app = App()
    app[0, 0] = buttons[0]
    app[0, 0] += buttons[1]


def test_set_tuple(buttons):
    """Set tuple of components to cell."""
    app = App()
    app[0, 0] = buttons[0], buttons[1]


def test_set_list(buttons):
    """Set list of components to cell."""
    app = App()
    app[0, 0] = [buttons[0], buttons[1]]


def test_append_no_init(buttons):
    """Append button to cell without component."""
    app = App()
    with pytest.raises(KeyError):
        app[0, 0] += buttons[0]


def test_append_to_partial(buttons):
    """Append button to partial cell."""
    app = App(columns=2)
    app[0] = buttons[0]
    with pytest.raises(KeyError):
        app[0, 0] += buttons[1]
    with pytest.raises(SpanOverlapError):
        app[0, 0] = buttons[1]


def test_append_to_partial_superset(buttons):
    """Append button to partial cell."""
    app = App(columns=2)
    app[0, 0] = buttons[0]
    with pytest.raises(Exception):
        app[0] += buttons[1]


def test_all_used(buttons):
    """Test all cells are used."""

    app = App(rows=2, columns=2)
    for i in range(4):
        app.add(buttons[i])

    check_all_cells_used(app._root)

    app = App(rows=2, columns=2)
    app[0, 0] = buttons[0]
    app[0, 1] = buttons[1]
    app[1, 0] = buttons[2]
    app[1, 1] = buttons[3]

    check_all_cells_used(app._root)

    app.add(buttons[2])

    assert len(app[1, 1]) == 2

    app = App(rows=2, columns=2)
    app[0] = buttons[0]
    app[1, 0] = buttons[2]
    app[1, 1] = buttons[3]

    check_all_cells_used(app._root)

    app.add(buttons[2])
    assert len(app[1, 1]) == 2


def test_used(buttons):
    """Test cell usage checks."""

    app = App(rows=2, columns=2)
    for i in range(3):
        app.add(buttons[i])

    app[0, 0] = buttons[3]
    app[0:1, 1] = buttons[3]
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
    assert count_used_cells(app._root) == 2
    app[0, :] = but
    assert count_used_cells(app._root) == 4

    app = App(rows=2, columns=2)
    app[0:1, 1:2] = but
    assert count_used_cells(app._root) == 1
    app[1:, 0:] = but
    assert count_used_cells(app._root) == 3

    app = App(rows=2, columns=2)
    app[-1, :2] = but
    assert count_used_cells(app._root) == 2

    app = App(rows=1, columns=2)
    app[0, :2] = but
    assert count_used_cells(app._root) == 2

    app = App(rows=1, columns=2)
    app[0] = but
    assert count_used_cells(app._root) == 2

    app = App(rows=2, columns=2)
    app[:2] = but
    assert count_used_cells(app._root) == 4
