"""Defines the App class."""

from typing import (  # pylint: disable=unused-import
    Any, Callable, Generator, List, Optional, Set, Tuple, Union, Dict, Sequence
)
import os
import json
import itertools
import shutil
from collections import namedtuple, defaultdict
from subprocess import Popen, PIPE, STDOUT, check_output
from pathlib import Path
import secrets
import socket
import warnings
import traceback

import eventlet
import msgpack
import flask
from flask import (
    Flask, render_template, make_response,
    copy_current_request_context, jsonify, request
)
from flask_socketio import SocketIO
from jinja2 import Environment, FileSystemLoader, ChoiceLoader

from bowtie._component import Event, Component, COMPONENT_REGISTRY
from bowtie.pager import Pager
from bowtie.exceptions import (
    GridIndexError, NoSidebarError,
    NotStatefulEvent, NoUnusedCellsError,
    SpanOverlapError, SizeError, WebpackError, YarnError
)

eventlet.monkey_patch(time=True)

Route = namedtuple('Route', ['view', 'path', 'exact'])
_Import = namedtuple('_Import', ['module', 'component'])

_DIRECTORY = Path('build')
_WEBPACK = './node_modules/.bin/webpack'
_MIN_NODE_VERSION = 6, 11, 5


class Scheduler:
    """Run scheduled tasks."""

    def __init__(self, app, seconds, func):
        """Create a scheduled function."""
        self.app = app
        self.seconds = seconds
        self.func = func
        self.thread = None

    def context(self, func):
        """Provide flask context to function."""
        def wrap():
            with self.app.app_context():
                func()
        return wrap

    def start(self):
        """Start the scheduled task."""
        self.thread = eventlet.spawn(self.run)

    def run(self):
        """Invoke the function repeatedly on a timer."""
        ret = eventlet.spawn(self.context(self.func))
        eventlet.sleep(self.seconds)
        try:
            ret.wait()
        except Exception:  # pylint: disable=broad-except
            traceback.print_exc()
        self.thread = eventlet.spawn(self.run)

    def stop(self):
        """Stop the scheduled task."""
        if self.thread:
            self.thread.cancel()


def raise_not_number(x: float) -> None:
    """Raise ``SizeError`` if ``x`` is not a number``."""
    try:
        float(x)
    except ValueError:
        raise SizeError('Must pass a number, received {}'.format(x))


class Span:
    """Define the location of a widget."""

    def __init__(self, row_start: int, column_start: int, row_end: Optional[int] = None,
                 column_end: Optional[int] = None) -> None:
        """Create a span for a widget.

        Indexing starts at 0. Start is inclusive and end is exclusive

        CSS Grid indexing starts at 1 and is [inclusive, exclusive)

        Note: `_start` and `_end` follow css grid naming convention.

        Parameters
        ----------
        row_start : int
        column_start : int
        row_end : int, optional
        column_end : int, optional

        """
        self.row_start = row_start
        self.column_start = column_start
        # add 1 to then ends because they start counting from 1
        if row_end is None:
            self.row_end = self.row_start + 1
        else:
            self.row_end = row_end
        if column_end is None:
            self.column_end = self.column_start + 1
        else:
            self.column_end = column_end

    @property
    def _key(self) -> Tuple[int, int, int, int]:
        return self.row_start, self.column_start, self.row_end, self.column_end

    def __hash__(self) -> int:
        """Hash for dict."""
        return hash(self._key)

    def __eq__(self, other) -> bool:
        """Compare eq for dict."""
        # pylint: disable=protected-access
        return isinstance(other, type(self)) and self._key == other._key

    def __repr__(self) -> str:
        """Show the starting and ending points.

        This is used as a key in javascript.
        """
        return '{},{},{},{}'.format(
            self.row_start + 1,
            self.column_start + 1,
            self.row_end + 1,
            self.column_end + 1
        )

    def overlap(self, other: 'Span'):
        """Detect if two spans overlap."""
        return not (
            # if one rectangle is left of other
            other.column_end <= self.column_start
            or self.column_end <= other.column_start
            # if one rectangle is above other
            or other.row_end <= self.row_start
            or self.row_end <= other.row_start
        )

    @property
    def cells(self) -> Generator[Tuple[int, int], None, None]:
        """Generate cells in span."""
        yield from itertools.product(
            range(self.row_start, self.row_end),
            range(self.column_start, self.column_end)
        )


class Size:
    """Size of rows and columns in grid.

    This is accessed through ``.rows`` and ``.columns`` from App and View instances.

    This uses CSS's minmax function.

    The minmax() CSS function defines a size range greater than or equal
    to min and less than or equal to max. If max < min, then max is ignored
    and minmax(min,max) is treated as min. As a maximum, a <flex> value
    sets the flex factor of a grid track; it is invalid as a minimum.

    Examples
    --------
    Laying out an app with the first row using 1/3 of the space
    and the second row using 2/3 of the space.

    >>> app = App(rows=2, columns=3)
    >>> app.rows[0].fraction(1)
    1fr
    >>> app.rows[1].fraction(2)
    2fr

    """

    def __init__(self) -> None:
        """Create a default row or column size with fraction = 1."""
        self.minimum: str = ''
        self.maximum: str = ''
        self.fraction(1)

    def auto(self) -> 'Size':
        """Set the size to auto or content based."""
        self.maximum = 'auto'
        return self

    def min_auto(self) -> 'Size':
        """Set the minimum size to auto or content based."""
        self.minimum = 'auto'
        return self

    def pixels(self, value: float) -> 'Size':
        """Set the size in pixels."""
        raise_not_number(value)
        self.maximum = '{}px'.format(value)
        return self

    def min_pixels(self, value: float) -> 'Size':
        """Set the minimum size in pixels."""
        raise_not_number(value)
        self.minimum = '{}px'.format(value)
        return self

    def ems(self, value: float) -> 'Size':
        """Set the size in ems."""
        raise_not_number(value)
        self.maximum = '{}em'.format(value)
        return self

    def min_ems(self, value: float) -> 'Size':
        """Set the minimum size in ems."""
        raise_not_number(value)
        self.minimum = '{}em'.format(value)
        return self

    def fraction(self, value: float) -> 'Size':
        """Set the fraction of free space to use."""
        raise_not_number(value)
        self.maximum = '{}fr'.format(value)
        return self

    def percent(self, value: float) -> 'Size':
        """Set the percentage of free space to use."""
        raise_not_number(value)
        self.maximum = '{}%'.format(value)
        return self

    def min_percent(self, value: float) -> 'Size':
        """Set the minimum percentage of free space to use."""
        raise_not_number(value)
        self.minimum = '{}%'.format(value)
        return self

    def __repr__(self) -> str:
        """Represent the size to be inserted into a JSX template."""
        if self.minimum:
            return 'minmax({}, {})'.format(self.minimum, self.maximum)
        return self.maximum


class Gap:
    """Margin between rows or columns of the grid.

    This is accessed through ``.row_gap`` and ``.column_gap`` from App and View instances.

    Examples
    --------
    Create a gap of 5 pixels between all rows.

    >>> app = App()
    >>> app.row_gap.pixels(5)
    5px

    """

    def __init__(self) -> None:
        """Create a default margin of zero."""
        self.gap: str = ''
        self.pixels(0)

    def pixels(self, value: int) -> 'Gap':
        """Set the margin in pixels."""
        raise_not_number(value)
        self.gap = '{}px'.format(value)
        return self

    def ems(self, value: int) -> 'Gap':
        """Set the margin in ems."""
        raise_not_number(value)
        self.gap = '{}em'.format(value)
        return self

    def percent(self, value) -> 'Gap':
        """Set the margin as a percentage."""
        raise_not_number(value)
        self.gap = '{}%'.format(value)
        return self

    def __repr__(self) -> str:
        """Represent the margin to be inserted into a JSX template."""
        return self.gap


def _check_index(value: int, length: int, bound: bool) -> int:
    if not isinstance(value, int):
        raise GridIndexError('Indices must be integers, found {}.'.format(value))
    if value < 0:
        value = value + length
    if value < 0 + bound or value >= length + bound:
        raise GridIndexError('Index out of range.')
    return value


def _slice_to_start_end(slc: slice, length: int) -> Tuple[int, int]:
    if slc.step is not None and slc.step != 1:
        raise GridIndexError(
            'slice step is not supported must be None or 1, was {}'.format(slc.step)
        )

    start = 0
    if slc.start is not None:
        start = slc.start

    end = length
    if slc.stop is not None:
        end = slc.stop
    return start, end


class Components:
    """List like class for storing components to override iadd.

    The purpose of this class is to override the `iadd` function.
    I want to be able to support all the following
    >>> from bowtie import App
    >>> from bowtie.control import Button
    >>> app = App()
    >>> button = Button()
    >>> app[0, 0] = button
    >>> app[0, 0] = button, button
    >>> app[0, 0] += button
    >>> app[0, 0] += button, button
    """

    TYPE_MSG: str = 'Must add a component or sequence of components, found {}.'

    def __init__(self,
                 component: Optional[Union[Component, Sequence[Component]]] = None
                 ) -> None:
        """Create a components list."""
        self.data: List[Component]
        if component is None:
            self.data = []
        elif isinstance(component, Component):
            self.data = [component]
        else:
            self.data = list(component)

    def __len__(self):
        """Count components."""
        return self.data.__len__()

    def append(self, component: Component):
        """Append component to the list."""
        return self.data.append(component)

    def __iter__(self):
        """Iterate over components."""
        return self.data.__iter__()

    def __getitem__(self, key):
        """Get item as a list."""
        return self.data.__getitem__(key)

    def _add(self, method, other: Union[Component, Sequence[Component]]) -> 'Components':
        if isinstance(other, Component):
            return method([other])
        if isinstance(other, Sequence):
            other = list(other)
            if not all(True for x in other if isinstance(x, Component)):
                raise TypeError(self.TYPE_MSG.format(other))
            return method(other)
        raise TypeError(self.TYPE_MSG.format(other))

    def __iadd__(self, other: Union[Component, Sequence[Component]]):
        """Append items to list when adding."""
        return self._add(self.data.__iadd__, other)

    def __add__(self, other: Union[Component, Sequence[Component]]):
        """Append items to list when adding."""
        return self._add(self.data.__add__, other)


class View:
    """Grid of components."""

    _NEXT_UUID = 0

    @classmethod
    def _next_uuid(cls) -> int:
        cls._NEXT_UUID += 1
        return cls._NEXT_UUID

    def __init__(self, rows: int = 1, columns: int = 1, sidebar: bool = False,
                 background_color: str = 'White') -> None:
        """Create a new grid.

        Parameters
        ----------
        rows : int, optional
            Number of rows in the grid.
        columns : int, optional
            Number of columns in the grid.
        sidebar : bool, optional
            Enable a sidebar for control components.
        background_color : str, optional
            Background color of the control pane.

        """
        self._uuid = View._next_uuid()
        self.layout = None
        self.column_gap = Gap()
        self.row_gap = Gap()
        self.border = Gap().pixels(7)
        self.rows = [Size() for _ in range(rows)]
        self.columns = [Size() for _ in range(columns)]
        self.sidebar = sidebar
        self.background_color = background_color
        self.layout: Optional[Callable] = None
        self._controllers: List[Component] = []
        self._spans: Dict[Span, Components] = {}

    def _all_components(self) -> Generator[Component, None, None]:
        yield from self._controllers
        yield from itertools.chain.from_iterable(self._spans.values())

    @property
    def _packages(self) -> Set[str]:
        # pylint: disable=protected-access
        packages = set(x._PACKAGE for x in self._all_components())
        packages.discard(None)
        return packages

    @property
    def _templates(self) -> Set[str]:
        # pylint: disable=protected-access
        return set(x._TEMPLATE for x in self._all_components())

    @property
    def _imports(self) -> Set[_Import]:
        # pylint: disable=protected-access
        return set(_Import(component=x._COMPONENT,
                           module=x._TEMPLATE[:x._TEMPLATE.find('.')])
                   for x in self._all_components())

    @property
    def _components(self) -> Set[Component]:
        return set(self._all_components())

    def _key_to_span(self, key: Any) -> Span:
        # TODO spaghetti code cleanup needed!
        if isinstance(key, Span):
            return key
        if isinstance(key, tuple):
            if len(key) == 1:
                return self._key_to_span(key[0])
            try:
                row_key, column_key = key
            except ValueError:
                raise GridIndexError('Index must be 1 or 2 values, found {}'.format(key))
            if isinstance(row_key, int):
                row_start = _check_index(row_key, len(self.rows), False)
                row_end = row_start + 1
            elif isinstance(row_key, slice):
                row_start, row_end = _slice_to_start_end(row_key, len(self.rows))
                row_start = _check_index(row_start, len(self.rows), False)
                row_end = _check_index(row_end, len(self.rows), True)
            else:
                raise GridIndexError(
                    'Cannot index with {}, pass in a int or a slice.'.format(row_key)
                )

            if isinstance(column_key, int):
                column_start = _check_index(column_key, len(self.columns), False)
                column_end = column_start + 1
            elif isinstance(column_key, slice):
                column_start, column_end = _slice_to_start_end(column_key, len(self.columns))
                column_start = _check_index(column_start, len(self.columns), False)
                column_end = _check_index(column_end, len(self.columns), True)
            else:
                raise GridIndexError(
                    'Cannot index with {}, pass in a int or a slice.'.format(column_key)
                )
            rows_cols = row_start, column_start, row_end, column_end

        elif isinstance(key, slice):
            start, end = _slice_to_start_end(key, len(self.rows))
            start = _check_index(start, len(self.rows), False)
            end = _check_index(end, len(self.rows), True)
            rows_cols = start, 0, end, len(self.columns)
        elif isinstance(key, int):
            row_start = _check_index(key, len(self.rows), False)
            rows_cols = row_start, 0, row_start + 1, len(self.columns)
        else:
            raise GridIndexError('Invalid index {}'.format(key))
        return Span(*rows_cols)

    def __getitem__(self, key: Any) -> Components:
        """Get item from the view."""
        span = self._key_to_span(key)
        if span not in self._spans:
            raise KeyError(f'Key {key} has not been used')
        return self._spans[span]

    def __setitem__(self, key: Any,
                    component: Union[Component, Sequence[Component]]) -> None:
        """Add widget to the view."""
        span = self._key_to_span(key)
        for used_span in self._spans:
            if span != used_span and span.overlap(used_span):
                raise SpanOverlapError(f'Spans {span} and {used_span} overlap. '
                                       'This is not permitted. '
                                       'If you want to do this please open an issue '
                                       'and explain your use case. '
                                       'https://github.com/jwkvam/bowtie/issues')
        self._spans[span] = Components(component)

    def add(self, component: Union[Component, Sequence[Component]]) -> None:
        """Add a widget to the grid in the next available cell.

        Searches over columns then rows for available cells.

        Parameters
        ----------
        components : bowtie._Component
            A Bowtie widget instance.

        """
        try:
            self[Span(*self._available_cell())] = component
        except NoUnusedCellsError:
            span = list(self._spans.keys())[-1]
            self._spans[span] += component

    def _available_cell(self) -> Tuple[int, int]:
        """Find next available cell first by row then column.

        First, construct a set containing all cells.
        Then iterate over the spans and remove occupied cells.
        """
        cells = set(itertools.product(range(len(self.rows)), range(len(self.columns))))
        for span in self._spans:
            for cell in span.cells:
                cells.remove(cell)

        if not cells:
            raise NoUnusedCellsError('No available cells')
        return min(cells)

    def add_sidebar(self, component: Component) -> None:
        """Add a widget to the sidebar.

        Parameters
        ----------
        component : bowtie._Component
            Add this component to the sidebar, it will be appended to the end.

        """
        if not self.sidebar:
            raise NoSidebarError('Set `sidebar=True` if you want to use the sidebar.')

        if not isinstance(component, Component):
            raise ValueError('component must be Component type, found {}'.format(component))
        # self._track_widget(widget)
        self._controllers.append(component)  # pylint: disable=protected-access

    @property
    def _columns_sidebar(self):
        columns = []
        if self.sidebar:
            columns.append(Size().ems(18))
        columns += self.columns
        return columns


class App:
    """Core class to layout, connect, build a Bowtie app."""

    def __init__(self, name='__main__', app=None, rows: int = 1, columns: int = 1,
                 sidebar: bool = False, title: str = 'Bowtie App',
                 theme: Optional[str] = None, background_color: str = 'White',
                 socketio: str = '', debug: bool = False) -> None:
        """Create a Bowtie App.

        Parameters
        ----------
        name : str, optional
            Use __name__ or leave as default if using a single module.
            Consult the Flask docs on "import_name" for details on more
            complex apps.
        app : Flask app, optional
            If you are defining your own Flask app, pass it in here.
            You only need this if you are doing other stuff with Flask
            outside of bowtie.
        row : int, optional
            Number of rows in the grid.
        columns : int, optional
            Number of columns in the grid.
        sidebar : bool, optional
            Enable a sidebar for control components.
        title : str, optional
            Title of the HTML.
        theme : str, optional
            Color for Ant Design components.
        background_color : str, optional
            Background color of the control pane.
        socketio : string, optional
            Socket.io path prefix, only change this for advanced deployments.
        debug : bool, optional
            Enable debugging in Flask. Disable in production!

        """
        self.title = title
        self.theme = theme
        self._init: Optional[Callable] = None
        self._socketio_path = socketio
        self._schedules: List[Scheduler] = []
        self._subscriptions: Dict[Event, List[Tuple[List[Event], Callable]]] = defaultdict(list)
        self._pages: Dict[Pager, Callable] = {}
        self._uploads: Dict[int, Callable] = {}
        self._root = View(rows=rows, columns=columns, sidebar=sidebar,
                          background_color=background_color)
        self._routes: List[Route] = []

        self._package_dir = Path(os.path.dirname(__file__))
        self._jinjaenv = Environment(
            loader=FileSystemLoader(str(self._package_dir / 'templates')),
            trim_blocks=True,
            lstrip_blocks=True
        )
        if app is None:
            self.app = Flask(name)
        else:
            self.app = app
        self.app.debug = debug
        self._socketio = SocketIO(self.app, binary=True, path=socketio + 'socket.io')
        self.app.secret_key = secrets.token_bytes()
        self.add_route(view=self._root, path='/', exact=True)

        # https://buxty.com/b/2012/05/custom-template-folders-with-flask/
        templates = Path(__file__).parent / 'templates'
        self.app.jinja_loader = ChoiceLoader([
            self.app.jinja_loader,
            FileSystemLoader(str(templates)),
        ])
        self._build_dir = self.app.root_path / _DIRECTORY
        self.app.before_first_request(self._endpoints)

    def wsgi_app(self, environ, start_response):
        """Support uwsgi and gunicorn."""
        return self.app.wsgi_app(environ, start_response)

    def __call__(self, environ, start_response):
        """Support uwsgi and gunicorn."""
        return self.wsgi_app(environ, start_response)

    def __getattr__(self, name: str):
        """Export attributes from root view."""
        if name == 'columns':
            return self._root.columns
        if name == 'rows':
            return self._root.rows
        if name == 'column_gap':
            return self._root.column_gap
        if name == 'row_gap':
            return self._root.row_gap
        if name == 'border':
            return self._root.border
        if name == 'layout':
            return self._root.layout
        raise AttributeError(name)

    def __setattr__(self, name, value):
        """Set layout function for root view."""
        if name == 'layout':
            return self._root.__setattr__(name, value)
        return super().__setattr__(name, value)

    def __getitem__(self, key: Any):
        """Get item from root view."""
        return self._root.__getitem__(key)

    def __setitem__(self, key: Any,
                    value: Union[Component, Sequence[Component]]) -> None:
        """Add widget to the root view."""
        self._root.__setitem__(key, value)

    def add(self, component: Component) -> None:
        """Add a widget to the grid in the next available cell.

        Searches over columns then rows for available cells.

        Parameters
        ----------
        component : bowtie._Component
            A Bowtie component instance.

        """
        self._root.add(component)

    def add_sidebar(self, widget: Component) -> None:
        """Add a widget to the sidebar.

        Parameters
        ----------
        widget : bowtie._Component
            Add this widget to the sidebar, it will be appended to the end.

        """
        self._root.add_sidebar(widget)

    def add_route(self, view: View, path: str, exact: bool = True) -> None:
        """Add a view to the app.

        Parameters
        ----------
        view : View
        path : str
        exact : bool, optional

        """
        if path[0] != '/':
            path = '/' + path
        for route in self._routes:
            assert path != route.path, 'Cannot use the same path twice'
        self._routes.append(Route(view=view, path=path, exact=exact))

        self.app.add_url_rule(
            path, path[1:], lambda: render_template('bowtie.html', title=self.title)
        )

    def subscribe(self, *events: Union[Event, Pager]) -> Callable:
        """Call a function in response to an event.

        If more than one event is given, `func` will be given
        as many arguments as there are events.

        If the pager calls notify, the decorated function will be called.

        Parameters
        ----------
        *event : event or pager
            Bowtie event, must have at least one.

        Examples
        --------
        Subscribing a function to multiple events.

        >>> from bowtie.control import Dropdown, Slider
        >>> app = App()
        >>> dd = Dropdown()
        >>> slide = Slider()
        >>> @app.subscribe(dd.on_change, slide.on_change)
        ... def callback(dd_item, slide_value):
        ...     pass
        >>> @app.subscribe(dd.on_change)
        ... @app.subscribe(slide.on_change)
        ... def callback2(value):
        ...     pass

        Using the pager to run a callback function.

        >>> from bowtie.pager import Pager
        >>> app = App()
        >>> pager = Pager()
        >>> @app.subscribe(pager)
        ... def callback():
        ...     pass
        >>> def scheduledtask():
        ...     pager.notify()

        """
        try:
            first_event = events[0]
        except IndexError:
            raise IndexError('Must subscribe to at least one event.')
        if len(events) != len(set(events)):
            raise ValueError(
                'Subscribed to the same event multiple times. All events must be unique.'
            )

        if len(events) > 1:
            # check if we are using any non stateful events
            for event in events:
                if isinstance(event, Pager):
                    raise NotStatefulEvent('Pagers must be subscribed by itself.')
                if event.getter is None:
                    raise NotStatefulEvent(
                        f'{event.uuid}.on_{event.name} is not a stateful event. '
                        'It must be used alone.'
                    )

        def decorator(func: Callable) -> Callable:
            """Handle three types of events: pages, uploads, and normal events."""
            if isinstance(first_event, Pager):
                self._pages[first_event] = func
            elif first_event.name == 'upload':
                if first_event.uuid in self._uploads:
                    warnings.warn(
                        ('Overwriting function "{func1}" with function '
                         '"{func2}" for upload object "{obj}".').format(
                             func1=self._uploads[first_event.uuid],
                             func2=func.__name__,
                             obj=COMPONENT_REGISTRY[first_event.uuid]
                         ), Warning)
                self._uploads[first_event.uuid] = func
            else:
                for event in events:
                    # need to have `events` here to maintain order of arguments
                    # not sure how to deal with mypy typing errors on events so ignoring
                    self._subscriptions[event].append((events, func))  # type: ignore
            return func

        return decorator

    def load(self, func: Callable) -> Callable:
        """Call a function on page load.

        Parameters
        ----------
        func : callable
            Function to be called.

        """
        self._init = func
        return func

    def schedule(self, seconds: float):
        """Call a function periodically.

        Parameters
        ----------
        seconds : float
            Minimum interval of function calls.
        func : callable
            Function to be called.

        """
        def wrap(func: Callable):
            self._schedules.append(Scheduler(self.app, seconds, func))
        return wrap

    def _write_templates(self) -> Set[str]:
        indexjsx = self._jinjaenv.get_template('index.jsx.j2')
        componentsjs = self._jinjaenv.get_template('components.js.j2')
        webpack = self._jinjaenv.get_template('webpack.common.js.j2')

        src = self._create_jspath()

        webpack_path = self._build_dir / webpack.name[:-3]  # type: ignore
        with webpack_path.open('w') as f:
            f.write(
                webpack.render(color=self.theme)
            )

        # copy js modules that are always needed
        for name in ['progress.jsx', 'view.jsx', 'utils.js']:
            template_src = self._package_dir / 'src' / name
            shutil.copy(template_src, src)

        # Layout Design
        #
        # Dictionaries that are keyed by the components
        #
        # To layout this will need to look through all components that have a key of the route
        #
        # use cases
        # 1. statically add items to controller in list
        # 2. remove item from controller
        # 3. add item back to controller
        #
        # issues:
        # widget reordering
        # order preserving operations

        components: Set[Component] = set()
        imports: Set[_Import] = set()
        packages: Set[str] = set()
        for route in self._routes:
            if route.view.layout:
                route.view.layout()
            packages |= route.view._packages  # pylint: disable=protected-access
            imports |= route.view._imports  # pylint: disable=protected-access
            components |= route.view._components  # pylint: disable=protected-access
            for template in route.view._templates:  # pylint: disable=protected-access
                template_src = self._package_dir / 'src' / template
                shutil.copy(template_src, src)

        with (src / componentsjs.name[:-3]).open('w') as f:  # type: ignore
            f.write(
                componentsjs.render(
                    imports=imports,
                    socketio=self._socketio_path,
                    components=components,
                )
            )

        with (src / indexjsx.name[:-3]).open('w') as f:  # type: ignore
            f.write(
                indexjsx.render(
                    maxviewid=View._NEXT_UUID,  # pylint: disable=protected-access
                    socketio=self._socketio_path,
                    pages=self._pages,
                    routes=self._routes,
                )
            )
        return packages

    def _build(self, notebook: Optional[str] = None) -> None:
        """Compile the Bowtie application."""
        if node_version() < _MIN_NODE_VERSION:
            raise WebpackError(
                f'Webpack requires at least version {_MIN_NODE_VERSION} of Node, '
                f'found version {node_version}.'
            )

        packages = self._write_templates()

        for filename in ['package.json', 'webpack.prod.js', 'webpack.dev.js']:
            if not (self._build_dir / filename).is_file():
                sourcefile = self._package_dir / 'src' / filename
                shutil.copy(sourcefile, self._build_dir)

        if self._run(['yarn', '--ignore-engines', 'install'], notebook=notebook) > 1:
            raise YarnError('Error installing node packages')

        if packages:
            installed = self._installed_packages()
            new_packages = [x for x in packages if x.split('@')[0] not in installed]

            if new_packages:
                retval = self._run(
                    ['yarn', '--ignore-engines', 'add'] + new_packages, notebook=notebook
                )
                if retval > 1:
                    raise YarnError('Error installing node packages')
                elif retval == 1:
                    print('Yarn error but trying to continue build')
        retval = self._run([_WEBPACK, '--config', 'webpack.dev.js'], notebook=notebook)
        if retval != 0:
            raise WebpackError('Error building with webpack')

    def _endpoints(self):
        def generate_sio_handler(main_event, supports):
            # get all events from all subscriptions associated with this event
            uniq_events = set()
            for events, _ in supports:
                uniq_events.update(events)
            uniq_events.remove(main_event)

            for event in uniq_events:
                comp = COMPONENT_REGISTRY[event.uuid]
                if event.getter is None:
                    raise AttributeError(
                        f'{comp} has no getter associated with event "on_{event.name}"'
                    )

            def handler(*args):
                def wrapuser():
                    event_data = {}
                    for event in uniq_events:
                        comp = COMPONENT_REGISTRY[event.uuid]
                        # we already checked that this component has a getter
                        event_data[event.signal] = getattr(comp, event.getter)()

                    # if there is no getter, then there is no data to unpack
                    # if there is a getter, then we need to unpack the data sent
                    main_getter = main_event.getter
                    if main_getter is not None:
                        comp = COMPONENT_REGISTRY[main_event.uuid]
                        event_data[main_event.signal] = getattr(comp, '_' + main_getter)(
                            msgpack.unpackb(args[0], encoding='utf8')
                        )

                    # gather the remaining data from the other events through their getter methods
                    for events, func in supports:
                        if main_getter is not None:
                            func(*(event_data[event.signal] for event in events))
                        else:
                            func()

                # TODO replace with flask socketio start_background_task
                eventlet.spawn(copy_current_request_context(wrapuser))
            return handler

        for event, supports in self._subscriptions.items():
            self._socketio.on(event.signal)(generate_sio_handler(event, supports))

        if self._init is not None:
            self._socketio.on('INITIALIZE')(lambda: eventlet.spawn(
                copy_current_request_context(self._init)
            ))

        def gen_upload(func):
            def upload():
                upfile = request.files['file']
                retval = func(upfile.filename, upfile.stream)
                if retval:
                    return make_response(jsonify(), 400)
                return make_response(jsonify(), 200)
            return upload

        for uuid, func in self._uploads.items():
            self.app.add_url_rule(
                f'/upload{uuid}', f'upload{uuid}', gen_upload(func), methods=['POST']
            )

        for page, func in self._pages.items():
            # pylint: disable=protected-access
            self._socketio.on(f'resp#{page._uuid}')(lambda: eventlet.spawn(
                copy_current_request_context(func)
            ))

        # bundle route
        @self.app.route('/bowtie/bundle.js')
        def bowtiebundlejs():  # pylint: disable=unused-variable
            bundle_path = self.app.root_path + '/build/bundle.js'
            bundle_path_gz = bundle_path + '.gz'

            try:
                if os.path.getmtime(bundle_path) > os.path.getmtime(bundle_path_gz):
                    return open(bundle_path, 'r').read()
                bundle = open(bundle_path_gz, 'rb').read()
                response = flask.make_response(bundle)
                response.headers['content-encoding'] = 'gzip'
                response.headers['vary'] = 'accept-encoding'
                response.headers['content-length'] = len(response.data)
                return response
            except FileNotFoundError:
                if os.path.isfile(bundle_path_gz):
                    bundle = open(bundle_path_gz, 'rb').read()
                    response = flask.make_response(bundle)
                    response.headers['Content-Encoding'] = 'gzip'
                    response.headers['Vary'] = 'Accept-Encoding'
                    response.headers['Content-Length'] = len(response.data)
                    return response
                return open(bundle_path, 'r').read()

        for schedule in self._schedules:
            schedule.start()

    def _serve(self, host='0.0.0.0', port=9991) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        if result == 0:
            raise Exception(f'Port {port} is unavailable on host {host}, aborting.')
        self._socketio.run(self.app, host=host, port=port)
        for schedule in self._schedules:
            schedule.stop()

    def _installed_packages(self) -> Generator[str, None, None]:
        """Extract installed packages as list from `package.json`."""
        with (self._build_dir / 'package.json').open('r') as f:
            packages = json.load(f)
        yield from packages['dependencies'].keys()

    def _create_jspath(self) -> Path:
        """Create the source directory for the build."""
        src = self._build_dir / 'bowtiejs'
        os.makedirs(src, exist_ok=True)
        return src

    def _run(self, command: List[str], notebook: Optional[str] = None) -> int:
        """Run command from terminal and notebook and view output from subprocess."""
        if notebook is None:
            return Popen(command, cwd=self._build_dir).wait()
        cmd = Popen(command, cwd=self._build_dir, stdout=PIPE, stderr=STDOUT)
        while True:
            line = cmd.stdout.readline()
            if line == b'' and cmd.poll() is not None:
                return cmd.poll()
            print(line.decode('utf-8'), end='')
        raise Exception()


def node_version():
    """Get node version."""
    version = check_output(('node', '--version'))
    return tuple(int(x) for x in version.strip()[1:].split(b'.'))
