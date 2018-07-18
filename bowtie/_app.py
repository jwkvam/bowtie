"""Defines the App class."""

from typing import (  # pylint: disable=unused-import
    Any, Callable, List, Optional, Set, Tuple, Union, Dict
)
import os
import json
from itertools import product
import inspect
import shutil
import stat
from collections import namedtuple, defaultdict, OrderedDict
from subprocess import Popen, PIPE, STDOUT
import warnings

from jinja2 import Environment, FileSystemLoader

from bowtie._component import Event, Component, COMPONENT_REGISTRY
from bowtie.exceptions import (
    GridIndexError, MissingRowOrColumn, NoSidebarError,
    NotStatefulEvent, UsedCellsError, NoUnusedCellsError,
    SizeError, WebpackError, YarnError
)
from bowtie.pager import Pager


_Import = namedtuple('_Import', ['module', 'component'])
_Control = namedtuple('_Control', ['instantiate', 'caption'])
_Schedule = namedtuple('_Schedule', ['seconds', 'function'])

_DIRECTORY = 'build'
_WEBPACK = './node_modules/.bin/webpack'


def raise_not_number(x: int) -> None:
    """Raise ``SizeError`` if ``x`` is not a number``."""
    try:
        float(x)
    except ValueError:
        raise SizeError('Must pass a number, received {}'.format(x))


class Span:
    """Define the location of a widget."""

    # pylint: disable=too-few-public-methods
    def __init__(self, row_start: int, column_start: int, row_end: Optional[int] = None,
                 column_end: Optional[int] = None) -> None:
        """Create a span for a widget.

        Indexing starts at 0. Both start and end are inclusive.

        Parameters
        ----------
        row_start : int
        column_start : int
        row_end : int, optional
        column_end : int, optional

        """
        self.row_start = row_start + 1
        self.column_start = column_start + 1
        # add 1 to then ends because they start counting from 1
        if row_end is None:
            self.row_end = self.row_start + 1
        else:
            self.row_end = row_end + 1
        if column_end is None:
            self.column_end = self.column_start + 1
        else:
            self.column_end = column_end + 1

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
        """Show the starting and ending points."""
        return '({}, {}) to ({}, {})'.format(
            self.row_start,
            self.column_start,
            self.row_end,
            self.column_end
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
        self.minimum = ''  # type: str
        self.maximum = ''  # type: str
        self.fraction(1)

    def auto(self) -> 'Size':
        """Set the size to auto or content based."""
        self.maximum = 'auto'
        return self

    def min_auto(self) -> 'Size':
        """Set the minimum size to auto or content based."""
        self.minimum = 'auto'
        return self

    def pixels(self, value) -> 'Size':
        """Set the size in pixels."""
        raise_not_number(value)
        self.maximum = '{}px'.format(value)
        return self

    def min_pixels(self, value) -> 'Size':
        """Set the minimum size in pixels."""
        raise_not_number(value)
        self.minimum = '{}px'.format(value)
        return self

    def ems(self, value) -> 'Size':
        """Set the size in ems."""
        raise_not_number(value)
        self.maximum = '{}em'.format(value)
        return self

    def min_ems(self, value) -> 'Size':
        """Set the minimum size in ems."""
        raise_not_number(value)
        self.minimum = '{}em'.format(value)
        return self

    def fraction(self, value: int) -> 'Size':
        """Set the fraction of free space to use as an integer."""
        raise_not_number(value)
        self.maximum = '{}fr'.format(int(value))
        return self

    def percent(self, value) -> 'Size':
        """Set the percentage of free space to use."""
        raise_not_number(value)
        self.maximum = '{}%'.format(value)
        return self

    def min_percent(self, value) -> 'Size':
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
        self.gap = ''  # type: str
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


class Widgets(list):
    """List for storing widgets to override iadd."""

    def __iadd__(self, other):
        """Append items to list when adding."""
        self.append(other)
        return self

    def __add__(self, other):
        """Append items to list when adding."""
        return self + [other]


class View:
    """Grid of widgets."""

    _NEXT_UUID = 0

    @classmethod
    def _next_uuid(cls) -> int:
        cls._NEXT_UUID += 1
        return cls._NEXT_UUID

    def __init__(self, rows: int = 1, columns: int = 1, sidebar: bool = True,
                 background_color: str = 'White') -> None:
        """Create a new grid.

        Parameters
        ----------
        rows : int, optional
            Number of rows in the grid.
        columns : int, optional
            Number of columns in the grid.
        sidebar : bool, optional
            Enable a sidebar for control widgets.
        background_color : str, optional
            Background color of the control pane.

        """
        self._uuid = View._next_uuid()
        self._used = OrderedDict(((key, False) for key in product(range(rows), range(columns))))
        self.column_gap = Gap()
        self.row_gap = Gap()
        self.rows = [Size() for _ in range(rows)]
        self.columns = [Size() for _ in range(columns)]
        self.sidebar = sidebar
        self.background_color = background_color
        self._packages = set()  # type: Set[str]
        self._templates = set()  # type: Set[str]
        self._imports = set()  # type: Set[_Import]
        self._controllers = []  # type: List[_Control]
        self._spans = defaultdict(Widgets)  # type: Dict[Span, List[Component]]

    @property
    def _name(self) -> str:
        return 'view{}.jsx'.format(self._uuid)

    def _key_to_rows_columns(self, key: Any) -> Tuple[int, int, int, int]:
        # TODO spaghetti code cleanup needed!
        if isinstance(key, tuple):
            if len(key) == 1:
                rows_cols = self._key_to_rows_columns(key[0])
            else:
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
        return rows_cols

    def __getitem__(self, key):
        """Get item from the view."""
        return self.spans[Span(*self._key_to_rows_columns(key))]

    def __setitem__(self, key: Any, widget: Component) -> None:
        """Add widget to the view."""
        if not isinstance(widget, Widgets):
            self._add(widget, *self._key_to_rows_columns(key))

    def add(self, widget: Component) -> None:
        """Add a widget to the grid in the next available cell.

        Searches over columns then rows for available cells.

        Parameters
        ----------
        widget : bowtie._Component
            A Bowtie widget instance.

        """
        self._add(widget)

    def _add(self, widget: Component, row_start: Optional[int] = None,
             column_start: Optional[int] = None, row_end: Optional[int] = None,
             column_end: Optional[int] = None) -> None:
        """Add a widget to the grid.

        Zero-based index and exclusive.

        Parameters
        ----------
        widget : bowtie._Component
            A Bowtie widget instance.
        row_start : int, optional
            Starting row for the widget.
        column_start : int, optional
            Starting column for the widget.
        row_end : int, optional
            Ending row for the widget.
        column_end : int, optional
            Ending column for the widget.

        """
        if not isinstance(widget, Component):
            raise ValueError('Widget must be a type of Component, found {}'.format(type(widget)))

        if row_start is not None and row_end is not None and row_start >= row_end:
            raise GridIndexError('row_start: {} must be less than row_end: {}'
                                 .format(row_start, row_end))
        if column_start is not None and column_end is not None and column_start >= column_end:
            raise GridIndexError('column_start: {} must be less than column_end: {}'
                                 .format(column_start, column_end))

        # pylint: disable=protected-access
        if widget._PACKAGE:
            self._packages.add(widget._PACKAGE)
        self._templates.add(widget._TEMPLATE)
        self._imports.add(_Import(component=widget._COMPONENT,
                                  module=widget._TEMPLATE[:widget._TEMPLATE.find('.')]))

        used_msg = 'Cell at [{}, {}] is already used.'
        if row_start is None or column_start is None:
            if row_start is not None:
                raise MissingRowOrColumn(
                    'Only row_start was defined. '
                    'Please specify both column_start and row_start or neither.'
                )
            if column_start is not None:
                raise MissingRowOrColumn(
                    'Only column_start was defined. '
                    'Please specify both column_start and row_start or neither.'
                )
            if row_end is not None or column_end is not None:
                raise MissingRowOrColumn(
                    'If you specify an end index you must '
                    'specify both row_start and column_start.'
                )
            row, col = None, None
            for (row, col), use in self._used.items():
                if not use:
                    break
            else:
                raise NoUnusedCellsError()
            span = Span(row, col)
            self._used[row, col] = True
        elif row_end is None and column_end is None:
            if self._used[row_start, column_start]:
                raise UsedCellsError(used_msg.format(row_start, column_start))
            span = Span(row_start, column_start)
            self._used[row_start, column_start] = True
        else:
            if row_end is None:
                row_end = row_start + 1
            if column_end is None:
                column_end = column_start + 1

            for row, col in product(range(row_start, row_end),
                                    range(column_start, column_end)):
                if self._used[row, col]:
                    raise UsedCellsError(used_msg.format(row, col))

            for row, col in product(range(row_start, row_end),
                                    range(column_start, column_end)):
                self._used[row, col] = True
            span = Span(row_start, column_start, row_end, column_end)

        self._spans[span].append(widget)

    def add_sidebar(self, widget: Component) -> None:
        """Add a widget to the sidebar.

        Parameters
        ----------
        widget : bowtie._Component
            Add this widget to the sidebar, it will be appended to the end.

        """
        if not self.sidebar:
            raise NoSidebarError('Set `sidebar=True` if you want to use the sidebar.')

        assert isinstance(widget, Component)

        # pylint: disable=protected-access
        if widget._PACKAGE:
            self._packages.add(widget._PACKAGE)
        self._templates.add(widget._TEMPLATE)
        self._imports.add(_Import(component=widget._COMPONENT,
                                  module=widget._TEMPLATE[:widget._TEMPLATE.find('.')]))
        self._controllers.append(_Control(instantiate=widget._instantiate,
                                          caption=getattr(widget, 'caption', None)))

    @property
    def _columns_sidebar(self):
        columns = []
        if self.sidebar:
            columns.append(Size().ems(18))
        columns += self.columns
        return columns

    def _render(self, path: str, env: Environment) -> None:
        """TODO: Docstring for _render.

        Parameters
        ----------
        path : TODO

        Returns
        -------
        TODO

        """
        jsx = env.get_template('view.jsx.j2')

        with open(os.path.join(path, self._name), 'w') as f:
            f.write(
                jsx.render(
                    uuid=self._uuid,
                    sidebar=self.sidebar,
                    background_color=self.background_color,
                    components=self._imports,
                    controls=self._controllers,
                    spans=self._spans
                )
            )


Route = namedtuple('Route', ['view', 'path', 'exact'])


class App:
    """Core class to layout, connect, build a Bowtie app."""

    def __init__(self, rows: int = 1, columns: int = 1, sidebar: bool = True,
                 title: str = 'Bowtie App', basic_auth: bool = False,
                 username: str = 'username', password: str = 'password',
                 theme: Optional[str] = None, background_color: str = 'White',
                 host: str = '0.0.0.0', port: int = 9991, socketio: str = '',
                 debug: bool = False) -> None:
        """Create a Bowtie App.

        Parameters
        ----------
        row : int, optional
            Number of rows in the grid.
        columns : int, optional
            Number of columns in the grid.
        sidebar : bool, optional
            Enable a sidebar for control widgets.
        title : str, optional
            Title of the HTML.
        basic_auth : bool, optional
            Enable basic authentication.
        username : str, optional
            Username for basic authentication.
        password : str, optional
            Password for basic authentication.
        theme : str, optional
            Color for Ant Design components.
        background_color : str, optional
            Background color of the control pane.
        host : str, optional
            Host IP address.
        port : int, optional
            Host port number.
        socketio : string, optional
            Socket.io path prefix, only change this for advanced deployments.
        debug : bool, optional
            Enable debugging in Flask. Disable in production!

        """
        self._basic_auth = basic_auth
        self._debug = debug
        self._host = host
        self._init = None
        self._password = password
        self._port = port
        self._socketio = socketio
        self._schedules = []  # type: List[_Schedule]
        self._subscriptions = defaultdict(list)  # type: Dict[Event, List[Tuple[List[Event], str]]]
        self._pages = {}  # type: Dict[Pager, str]
        self._title = title
        self._username = username
        self._uploads = {}  # type: Dict[int, str]
        self.theme = theme
        self._root = View(rows=rows, columns=columns, sidebar=sidebar,
                          background_color=background_color)
        self._routes = [Route(view=self._root, path='/', exact=True)]
        self._package_dir = os.path.dirname(__file__)
        self._jinjaenv = Environment(
            loader=FileSystemLoader(os.path.join(self._package_dir, 'templates')),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def __getattr__(self, name: str) -> Union[Gap, List[Size]]:
        """Export attributes from root view."""
        if name == 'columns':
            return self._root.columns
        if name == 'rows':
            return self._root.rows
        if name == 'column_gap':
            return self._root.column_gap
        if name == 'row_gap':
            return self._root.row_gap
        raise AttributeError(name)

    def __getitem__(self, key):
        """Get item from root view."""
        return self._root.__getitem__(key)

    def __setitem__(self, key: Any, value: Component) -> None:
        """Add widget to the root view."""
        self._root.__setitem__(key, value)

    def add(self, widget: Component) -> None:
        """Add a widget to the grid in the next available cell.

        Searches over columns then rows for available cells.

        Parameters
        ----------
        widget : bowtie._Component
            A Bowtie widget instance.

        """
        self._root.add(widget)

    def add_sidebar(self, widget: Component) -> None:
        """Add a widget to the sidebar.

        Parameters
        ----------
        widget : bowtie._Component
            Add this widget to the sidebar, it will be appended to the end.

        """
        self._root.add_sidebar(widget)

    def add_route(self, view, path, exact=True):
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

    def respond(self, pager: Pager, func: Callable) -> None:
        """Call a function in response to a page.

        When the pager calls notify, the function will be called.

        Parameters
        ----------
        pager : Pager
            Pager that to signal when func is called.
        func : callable
            Function to be called.

        Examples
        --------
        Using the pager to run a callback function.

        >>> from bowtie.pager import Pager
        >>> app = App()
        >>> pager = Pager()
        >>> def callback():
        ...     pass
        >>> def scheduledtask():
        ...     pager.notify()
        >>> app.respond(pager, callback)

        """
        self._pages[pager] = func.__name__

    def subscribe(self, func: Callable, event: Event, *events: Event) -> None:
        """Call a function in response to an event.

        If more than one event is given, `func` will be given
        as many arguments as there are events.

        Parameters
        ----------
        func : callable
            Function to be called.
        event : event
            A Bowtie event.
        *events : Each is an event, optional
            Additional events.

        Examples
        --------
        Subscribing a function to multiple events.

        >>> from bowtie.control import Dropdown, Slider
        >>> app = App()
        >>> dd = Dropdown()
        >>> slide = Slider()
        >>> def callback(dd_item, slide_value):
        ...     pass
        >>> app.subscribe(callback, dd.on_change, slide.on_change)

        """
        all_events = [event, *events]
        if len(all_events) != len(set(all_events)):
            raise ValueError('Subscribed to the same event multiple times. '
                             'All events must be unique.')

        if len(all_events) > 1:
            # check if we are using any non stateful events
            for evt in all_events:
                if evt.getter is None:
                    msg = '{}.on_{} is not a stateful event. It must be used alone.'
                    raise NotStatefulEvent(msg.format(evt.uuid, evt.name))

        if event.name == 'upload':
            if event.uuid in self._uploads:
                warnings.warn(
                    ('Overwriting function "{func1}" with function '
                     '"{func2}" for upload object "{obj}".').format(
                         func1=self._uploads[event.uuid],
                         func2=func.__name__,
                         obj=COMPONENT_REGISTRY[event.uuid]
                     ), Warning)
            self._uploads[event.uuid] = func.__name__

        for evt in all_events:
            self._subscriptions[evt].append((all_events, func.__name__))

    def listen(self, event: Event, *events: Event) -> Callable:
        """Call a function in response to an event.

        If more than one event is given, `func` will be given
        as many arguments as there are events.

        Parameters
        ----------
        event : event
            A Bowtie event.
        *events : Each is an event, optional
            Additional events.

        Examples
        --------
        Subscribing a function to multiple events.

        >>> from bowtie.control import Dropdown, Slider
        >>> app = App()
        >>> dd = Dropdown()
        >>> slide = Slider()
        >>> @app.listen(dd.on_change, slide.on_change)
        ... def callback(dd_item, slide_value):
        ...     pass
        >>> @app.listen(dd.on_change)
        ... @app.listen(slide.on_change)
        ... def callback2(value):
        ...     pass

        """
        def decorator(func):
            """Subscribe function to events."""
            self.subscribe(func, event, *events)
            return func
        return decorator

    def load(self, func):
        """Call a function on page load.

        Parameters
        ----------
        func : callable
            Function to be called.

        """
        self._init = func.__name__

    def schedule(self, seconds, func):
        """Call a function periodically.

        Parameters
        ----------
        seconds : float
            Minimum interval of function calls.
        func : callable
            Function to be called.

        """
        self._schedules.append(_Schedule(seconds, func.__name__))

    def _sourcefile(self):  # pylint: disable=no-self-use
        # [-1] grabs the top of the stack
        return os.path.basename(inspect.stack()[-1].filename)[:-3]

    def _write_templates(self, notebook: Optional[str] = None) -> Set[str]:
        server = self._jinjaenv.get_template('server.py.j2')
        indexhtml = self._jinjaenv.get_template('index.html.j2')
        indexjsx = self._jinjaenv.get_template('index.jsx.j2')
        webpack = self._jinjaenv.get_template('webpack.common.js.j2')

        src, app, templates = create_directories()

        webpack_path = os.path.join(_DIRECTORY, webpack.name[:-3])  # type: ignore
        with open(webpack_path, 'w') as f:
            f.write(
                webpack.render(color=self.theme)
            )

        server_path = os.path.join(src, server.name[:-3])  # type: ignore
        with open(server_path, 'w') as f:
            f.write(
                server.render(
                    socketio=self._socketio,
                    basic_auth=self._basic_auth,
                    username=self._username,
                    password=self._password,
                    notebook=notebook,
                    source_module=self._sourcefile() if not notebook else None,
                    subscriptions=self._subscriptions,
                    uploads=self._uploads,
                    schedules=self._schedules,
                    initial=self._init,
                    routes=self._routes,
                    pages=self._pages,
                    host="'{}'".format(self._host),
                    port=self._port,
                    debug=self._debug
                )
            )

        perms = os.stat(server_path)
        os.chmod(server_path, perms.st_mode | stat.S_IEXEC)

        template_src = os.path.join(self._package_dir, 'src', 'progress.jsx')
        shutil.copy(template_src, app)
        template_src = os.path.join(self._package_dir, 'src', 'utils.js')
        shutil.copy(template_src, app)
        for route in self._routes:
            # pylint: disable=protected-access
            for template in route.view._templates:
                template_src = os.path.join(self._package_dir, 'src', template)
                shutil.copy(template_src, app)

        packages = set()  # type: Set[str]
        for route in self._routes:
            route.view._render(app, self._jinjaenv)  # pylint: disable=protected-access
            packages |= route.view._packages  # pylint: disable=protected-access

        with open(os.path.join(templates, indexhtml.name[:-3]), 'w') as f:  # type: ignore
            f.write(
                indexhtml.render(
                    title=self._title,
                )
            )

        with open(os.path.join(app, indexjsx.name[:-3]), 'w') as f:  # type: ignore
            f.write(
                indexjsx.render(
                    maxviewid=View._NEXT_UUID,  # pylint: disable=protected-access
                    socketio=self._socketio,
                    pages=self._pages,
                    routes=self._routes
                )
            )
        return packages

    def _build(self, notebook: None = None) -> None:
        """Compile the Bowtie application."""
        packages = self._write_templates(notebook=notebook)

        if not os.path.isfile(os.path.join(_DIRECTORY, 'package.json')):
            packagejson = os.path.join(self._package_dir, 'src/package.json')
            shutil.copy(packagejson, _DIRECTORY)

        if not os.path.isfile(os.path.join(_DIRECTORY, 'webpack.prod.json')):
            webpackprod = os.path.join(self._package_dir, 'src/webpack.prod.js')
            shutil.copy(webpackprod, _DIRECTORY)

        if not os.path.isfile(os.path.join(_DIRECTORY, 'webpack.dev.json')):
            webpackdev = os.path.join(self._package_dir, 'src/webpack.dev.js')
            shutil.copy(webpackdev, _DIRECTORY)

        if run(['yarn', '--ignore-engines', 'install'], notebook=notebook) > 1:
            raise YarnError('Error installing node packages')

        if packages:
            installed = installed_packages()
            new_packages = [x for x in packages if x.split('@')[0] not in installed]

            if new_packages:
                retval = run(['yarn', '--ignore-engines', 'add'] + new_packages, notebook=notebook)
                if retval > 1:
                    raise YarnError('Error installing node packages')
                elif retval == 1:
                    print('Yarn error but trying to continue build')
        retval = run([_WEBPACK, '--config', 'webpack.dev.js'], notebook=notebook)
        if retval != 0:
            raise WebpackError('Error building with webpack')


def run(command: List[str], notebook: None = None) -> int:
    """Run command from terminal and notebook and view output from subprocess."""
    if notebook is None:
        return Popen(command, cwd=_DIRECTORY).wait()
    cmd = Popen(command, cwd=_DIRECTORY, stdout=PIPE, stderr=STDOUT)
    while True:
        line = cmd.stdout.readline()
        if line == b'' and cmd.poll() is not None:
            return cmd.poll()
        print(line.decode('utf-8'), end='')
    raise Exception()


def installed_packages():
    """Extract installed packages as list from `package.json`."""
    with open(os.path.join(_DIRECTORY, 'package.json'), 'r') as f:
        packagejson = json.load(f)
    return packagejson['dependencies'].keys()


def create_directories() -> Tuple[str, str, str]:
    """Create all the necessary subdirectories for the build."""
    src = os.path.join(_DIRECTORY, 'src')
    templates = os.path.join(src, 'templates')
    app = os.path.join(src, 'app')
    os.makedirs(app, exist_ok=True)
    os.makedirs(templates, exist_ok=True)
    return src, app, templates
