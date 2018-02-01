# -*- coding: utf-8 -*-
"""Defines the App class."""

from __future__ import print_function

import os
import json
from itertools import product
import inspect
import shutil
import stat
from collections import namedtuple, defaultdict, OrderedDict
from subprocess import Popen
import warnings

from jinja2 import Environment, FileSystemLoader

from bowtie._compat import makedirs
from bowtie._component import Component, SEPARATOR


_Import = namedtuple('_Import', ['module', 'component'])
_Control = namedtuple('_Control', ['instantiate', 'caption'])
_Schedule = namedtuple('_Schedule', ['seconds', 'function'])

_DIRECTORY = 'build'
_WEBPACK = './node_modules/.bin/webpack'


class YarnError(Exception):
    """Errors from ``Yarn``."""

    pass


class WebpackError(Exception):
    """Errors from ``Webpack``."""

    pass


class SizeError(Exception):
    """Size values must be a number."""

    pass


class GridIndexError(Exception):
    """Invalid index into the grid layout."""

    pass


class NoUnusedCellsError(Exception):
    """All cells are used."""

    pass


class UsedCellsError(Exception):
    """All cells are used."""

    pass


class MissingRowOrColumn(Exception):
    """Missing a row or column."""

    pass


class NoSidebarError(Exception):
    """Cannot add to the sidebar when it doesn't exist."""

    pass


class NotStatefulEvent(Exception):
    """This event is not stateful and cannot be paired with other events."""

    pass


def raise_not_number(x):
    """Raise ``SizeError`` if ``x`` is not a number``."""
    try:
        float(x)
    except ValueError:
        raise SizeError('Must pass a number, received {}'.format(x))


class Span(object):
    """Define the location of a widget."""

    # pylint: disable=too-few-public-methods
    def __init__(self, row_start, column_start, row_end=None, column_end=None):
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
        # add 2 to then ends because they start counting from 1
        # and they are exclusive
        if row_end is None:
            self.row_end = row_start + 2
        else:
            self.row_end = row_end + 2
        if column_end is None:
            self.column_end = column_start + 2
        else:
            self.column_end = column_end + 2

    def __repr__(self):
        """Show the starting and ending points."""
        return '({}, {}) to ({}, {})'.format(
            self.row_start,
            self.column_start,
            self.row_end,
            self.column_end
        )


class Size(object):
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
    >>> app.rows[1].fraction(2)

    """

    def __init__(self):
        """Create a default row or column size with fraction = 1."""
        self.minimum = None
        self.maximum = None
        self.fraction(1)

    def auto(self):
        """Set the size to auto or content based."""
        self.maximum = 'auto'

    def min_auto(self):
        """Set the minimum size to auto or content based."""
        self.minimum = 'auto'

    def pixels(self, value):
        """Set the size in pixels."""
        raise_not_number(value)
        self.maximum = '{}px'.format(value)

    def min_pixels(self, value):
        """Set the minimum size in pixels."""
        raise_not_number(value)
        self.minimum = '{}px'.format(value)

    def fraction(self, value):
        """Set the fraction of free space to use as an integer."""
        raise_not_number(value)
        self.maximum = '{}fr'.format(int(value))

    def percent(self, value):
        """Set the percentage of free space to use."""
        raise_not_number(value)
        self.maximum = '{}%'.format(value)

    def min_percent(self, value):
        """Set the minimum percentage of free space to use."""
        raise_not_number(value)
        self.minimum = '{}%'.format(value)

    def __repr__(self):
        """Represent the size to be inserted into a JSX template."""
        if self.minimum:
            return 'minmax({}, {})'.format(self.minimum, self.maximum)
        return self.maximum


class Gap(object):
    """Margin between rows or columns of the grid.

    This is accessed through ``.row_gap`` and ``.column_gap`` from App and View instances.

    Examples
    --------
    Create a gap of 5 pixels between all rows.

    >>> app = App()
    >>> app.row_gap.pixels(5)

    """

    def __init__(self):
        """Create a default margin of zero."""
        self.gap = None
        self.pixels(0)

    def pixels(self, value):
        """Set the margin in pixels."""
        raise_not_number(value)
        self.gap = '{}px'.format(value)

    def percent(self, value):
        """Set the margin as a percentage."""
        raise_not_number(value)
        self.gap = '{}%'.format(value)

    def __repr__(self):
        """Represent the margin to be inserted into a JSX template."""
        return self.gap


class View(object):
    """Grid of widgets."""

    _NEXT_UUID = 0

    @classmethod
    def _next_uuid(cls):
        cls._NEXT_UUID += 1
        return cls._NEXT_UUID

    def __init__(self, rows=1, columns=1, sidebar=True,
                 background_color='White'):
        """Create a new grid."""
        self._uuid = View._next_uuid()
        self.used = OrderedDict(((key, False) for key in product(range(rows), range(columns))))
        self.column_gap = Gap()
        self.row_gap = Gap()
        self.rows = [Size() for _ in range(rows)]
        self.columns = [Size() for _ in range(columns)]
        self.sidebar = sidebar
        self.background_color = background_color
        self.packages = set()
        self.templates = set()
        self.imports = set()
        self.controllers = []
        self.widgets = []
        self.spans = []

    @property
    def _name(self):
        return 'view{}.jsx'.format(self._uuid)

    def add(self, widget, row_start=None, column_start=None,
            row_end=None, column_end=None):
        """Add a widget to the grid.

        Zero-based index and inclusive.

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
        assert isinstance(widget, Component)

        for index in [row_start, row_end]:
            if index is not None and not 0 <= index < len(self.rows):
                raise GridIndexError('Invalid Row Index')
        for index in [column_start, column_end]:
            if index is not None and not 0 <= index < len(self.columns):
                raise GridIndexError('Invalid Column Index')

        if row_start is not None and row_end is not None and row_start > row_end:
            raise GridIndexError('Invalid Column Index')
        if column_start is not None and column_end is not None and column_start > column_end:
            raise GridIndexError('Invalid Column Index')

        # pylint: disable=protected-access
        self.packages.add(widget._PACKAGE)
        self.templates.add(widget._TEMPLATE)
        self.imports.add(_Import(component=widget._COMPONENT,
                                 module=widget._TEMPLATE[:widget._TEMPLATE.find('.')]))

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
            for (row, col), use in self.used.items():
                if not use:
                    break
            else:
                raise NoUnusedCellsError()
            span = Span(row, col)
            self.used[row, col] = True
        elif row_end is None and column_end is None:
            if self.used[row_start, column_start]:
                raise UsedCellsError('Cell at {}, {} is already used.'
                                     .format(row_start, column_start))
            span = Span(row_start, column_start)
            self.used[row_start, column_start] = True
        else:
            if row_end is None:
                row_end = row_start
            if column_end is None:
                column_end = column_start

            for row, col in product(range(row_start, row_end + 1),
                                    range(column_start, column_end + 1)):
                if self.used[row, col]:
                    raise UsedCellsError('Cell at {}, {} is already used.'.format(row, col))

            for row, col in product(range(row_start, row_end + 1),
                                    range(column_start, column_end + 1)):
                self.used[row, col] = True
            span = Span(row_start, column_start, row_end, column_end)

        self.widgets.append(widget)
        self.spans.append(span)

    def add_sidebar(self, widget):
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
        self.packages.add(widget._PACKAGE)
        self.templates.add(widget._TEMPLATE)
        self.imports.add(_Import(component=widget._COMPONENT,
                                 module=widget._TEMPLATE[:widget._TEMPLATE.find('.')]))
        self.controllers.append(_Control(instantiate=widget._instantiate,
                                         caption=getattr(widget, 'caption', None)))

    def _render(self, path, env):
        """TODO: Docstring for _render.

        Parameters
        ----------
        path : TODO

        Returns
        -------
        TODO

        """
        jsx = env.get_template('view.jsx.j2')

        # pylint: disable=protected-access
        self.widgets = [w._instantiate for w in self.widgets]

        columns = []
        if self.sidebar:
            columns.append('18em')
        columns += self.columns

        with open(os.path.join(path, self._name), 'w') as f:
            f.write(
                jsx.render(
                    uuid=self._uuid,
                    sidebar=self.sidebar,
                    columns=columns,
                    rows=self.rows,
                    column_gap=self.column_gap,
                    row_gap=self.row_gap,
                    background_color=self.background_color,
                    components=self.imports,
                    controls=self.controllers,
                    widgets=zip(self.widgets, self.spans)
                )
            )


Route = namedtuple('Route', ['view', 'path', 'exact'])


class App(object):
    """Core class to layout, connect, build a Bowtie app."""

    def __init__(self, rows=1, columns=1, sidebar=True,
                 title='Bowtie App', basic_auth=False,
                 username='username', password='password',
                 background_color='White', host='0.0.0.0', port=9991,
                 socketio='', debug=False):
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
        self.background_color = background_color
        self.basic_auth = basic_auth
        self.debug = debug
        self.functions = []
        self.host = host
        self.imports = set()
        self.init = None
        self.password = password
        self.port = port
        self.socketio = socketio
        self.schedules = []
        self.subscriptions = defaultdict(list)
        self.pages = {}
        self.title = title
        self.username = username
        self.uploads = {}
        self.root = View(rows=rows, columns=columns, sidebar=sidebar,
                         background_color=background_color)
        self.routes = [Route(view=self.root, path='/', exact=True)]
        self._package_dir = os.path.dirname(__file__)
        self._jinjaenv = Environment(
            loader=FileSystemLoader(os.path.join(self._package_dir, 'templates')),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def __getattr__(self, name):
        """Export attributes from root view."""
        if name == 'columns':
            return self.root.columns
        elif name == 'rows':
            return self.root.rows
        elif name == 'column_gap':
            return self.root.column_gap
        elif name == 'row_gap':
            return self.root.row_gap
        else:
            raise AttributeError(name)

    def add(self, widget, row_start=None, column_start=None,
            row_end=None, column_end=None):
        """Add a widget to the grid.

        Zero-based index and inclusive.

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
        self.root.add(widget, row_start=row_start, column_start=column_start,
                      row_end=row_end, column_end=column_end)

    def add_sidebar(self, widget):
        """Add a widget to the sidebar.

        Parameters
        ----------
        widget : bowtie._Component
            Add this widget to the sidebar, it will be appended to the end.

        """
        self.root.add_sidebar(widget)

    def add_route(self, view, path, exact=True):
        """Add a view to the app.

        Parameters
        ----------
        view : View
        path : str
        exact : bool, optional

        """
        assert path[0] == '/'
        for route in self.routes:
            assert path != route.path, 'Cannot use the same path twice'
        self.routes.append(Route(view=view, path=path, exact=exact))

    def respond(self, pager, func):
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
        self.pages[pager] = func.__name__

    def subscribe(self, func, event, *events):
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
        all_events = [event]
        all_events.extend(events)

        if len(all_events) > 1:
            # check if we are using any non stateful events
            for evt in all_events:
                if evt[2] is None:
                    name = evt[0].split(SEPARATOR)[1]
                    msg = '{}.on_{} is not a stateful event. It must be used alone.'
                    raise NotStatefulEvent(msg.format(evt[1], name))

        if event[0].split(SEPARATOR)[1] == 'upload':
            # evt = event[0]
            uuid = event[0].split(SEPARATOR)[0]
            if uuid in self.uploads:
                warnings.warn(
                    ('Overwriting function "{func1}" with function '
                     '"{func2}" for upload object "{obj}".').format(
                         func1=self.uploads[uuid],
                         func2=func.__name__,
                         obj=event[1]
                     ), Warning)
            self.uploads[uuid] = func.__name__

        for evt in all_events:
            self.subscriptions[evt].append((all_events, func.__name__))

    def load(self, func):
        """Call a function on page load.

        Parameters
        ----------
        func : callable
            Function to be called.

        """
        self.init = func.__name__

    def schedule(self, seconds, func):
        """Call a function periodically.

        Parameters
        ----------
        seconds : float
            Minimum interval of function calls.
        func : callable
            Function to be called.

        """
        self.schedules.append(_Schedule(seconds, func.__name__))

    # pylint: disable=no-self-use
    def _sourcefile(self):
        # [-1] grabs the top of the stack and [1] grabs the filename
        return os.path.basename(inspect.stack()[-1][1])[:-3]

    def _write_templates(self):
        server = self._jinjaenv.get_template('server.py.j2')
        indexhtml = self._jinjaenv.get_template('index.html.j2')
        indexjsx = self._jinjaenv.get_template('index.jsx.j2')

        src, app, templates = create_directories()

        server_path = os.path.join(src, server.name[:-3])
        with open(server_path, 'w') as f:
            f.write(
                server.render(
                    socketio=self.socketio,
                    basic_auth=self.basic_auth,
                    username=self.username,
                    password=self.password,
                    source_module=self._sourcefile(),
                    subscriptions=self.subscriptions,
                    uploads=self.uploads,
                    schedules=self.schedules,
                    initial=self.init,
                    routes=self.routes,
                    pages=self.pages,
                    host="'{}'".format(self.host),
                    port=self.port,
                    debug=self.debug
                )
            )

        perms = os.stat(server_path)
        os.chmod(server_path, perms.st_mode | stat.S_IEXEC)

        template_src = os.path.join(self._package_dir, 'src', 'progress.jsx')
        shutil.copy(template_src, app)
        template_src = os.path.join(self._package_dir, 'src', 'utils.js')
        shutil.copy(template_src, app)
        for route in self.routes:
            for template in route.view.templates:
                template_src = os.path.join(self._package_dir, 'src', template)
                shutil.copy(template_src, app)

        packages = set()
        for route in self.routes:
            # pylint: disable=protected-access
            route.view._render(app, self._jinjaenv)
            packages |= route.view.packages

        with open(os.path.join(templates, indexhtml.name[:-3]), 'w') as f:
            f.write(
                indexhtml.render(
                    title=self.title,
                )
            )

        with open(os.path.join(app, indexjsx.name[:-3]), 'w') as f:
            f.write(
                indexjsx.render(
                    # pylint: disable=protected-access
                    maxviewid=View._NEXT_UUID,
                    socketio=self.socketio,
                    pages=self.pages,
                    routes=self.routes
                )
            )
        return packages

    def build(self):
        """Deprecate build function."""
        warnings.warn(
            '`build` is deprecated, return the `App` object instead.',
            DeprecationWarning
        )

    def _build(self):
        """Compile the Bowtie application."""
        packages = self._write_templates()

        if not os.path.isfile(os.path.join(_DIRECTORY, 'webpack.config.js')):
            webpack_src = os.path.join(self._package_dir, 'src/webpack.config.js')
            shutil.copy(webpack_src, _DIRECTORY)

        if not os.path.isfile(os.path.join(_DIRECTORY, 'package.json')):
            packagejson = os.path.join(self._package_dir, 'src/package.json')
            shutil.copy(packagejson, _DIRECTORY)

        install = Popen('yarn install', shell=True, cwd=_DIRECTORY).wait()
        if install > 1:
            raise YarnError('Error install node packages')

        packages.discard(None)
        if packages:
            installed = installed_packages()
            packages = [x for x in packages if x.split('@')[0] not in installed]

            if packages:
                packagestr = ' '.join(packages)
                install = Popen('yarn add {}'.format(packagestr),
                                shell=True, cwd=_DIRECTORY).wait()
                if install > 1:
                    raise YarnError('Error install node packages')
                elif install == 1:
                    print('Yarn error but trying to continue build')
        dev = Popen('{} -d'.format(_WEBPACK), shell=True, cwd=_DIRECTORY).wait()
        if dev != 0:
            raise WebpackError('Error building with webpack')


def installed_packages():
    """Extract installed packages as list from `package.json`."""
    with open(os.path.join(_DIRECTORY, 'package.json'), 'r') as f:
        packagejson = json.load(f)
    return packagejson['dependencies'].keys()


def create_directories():
    """Create all the necessary subdirectories for the build."""
    src = os.path.join(_DIRECTORY, 'src')
    templates = os.path.join(src, 'templates')
    app = os.path.join(src, 'app')
    makedirs(app, exist_ok=True)
    makedirs(templates, exist_ok=True)
    return src, app, templates
