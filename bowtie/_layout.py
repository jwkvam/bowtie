# -*- coding: utf-8 -*-
"""
Defines the Layout class.
"""

from __future__ import print_function

import os
from os import path
import inspect
import shutil
import stat
from collections import namedtuple, defaultdict
from subprocess import Popen

from flask import Markup
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

from bowtie._compat import makedirs
from bowtie.control import _Controller
from bowtie.visual import _Visual


_Import = namedtuple('_Import', ['module', 'component'])
_Control = namedtuple('_Control', ['instantiate', 'caption'])
_Schedule = namedtuple('_Control', ['seconds', 'function'])


class YarnError(Exception):
    """
    Errors from ``Yarn``.
    """
    pass


class WebpackError(Exception):
    """
    Errors from ``Webpack``.
    """
    pass


class Layout(object):
    """Create a Bowtie App.

    Parameters
    ----------
    title : str, optional
        Title of the HTML.
    description : str, optional
        Describe the app in Markdown, inserted in control pane.
    basic_auth : bool, optional
        Enable basic authentication.
    username : str, optional
        Username for basic authentication.
    password : str, optional
        Password for basic authentication.
    background_color : str, optional
        Background color of the control pane.
    directory : str, optional
        Location where app is compiled.
    host : str, optional
        Host IP address.
    port : int, optional
        Host port number.
    debug : bool, optional
        Enable debugging in Flask. Disable in production!

    """

    _packages = [
        'antd',
        'babel-core',
        'babel-loader',
        'babel-plugin-transform-object-rest-spread',
        'babel-polyfill',
        'babel-preset-es2015',
        'babel-preset-react',
        'babel-preset-stage-0',
        'classnames',
        'core-js',
        'css-loader',
        'extract-text-webpack-plugin',
        'less',
        'less-loader',
        'lodash.clonedeep',
        'msgpack-lite',
        'node-sass',
        'normalize.css',
        'postcss-modules-values',
        'react',
        'react-dom',
        'sass-loader',
        'socket.io-client',
        'style-loader',
        'webpack@1.14.0'
    ]

    def __init__(self, title='Bowtie App', description='Bowtie App\n---',
                 basic_auth=False, username='username', password='password',
                 background_color='White', directory='build',
                 host='0.0.0.0', port=9991, debug=False):
        self.background_color = background_color
        self.basic_auth = basic_auth
        self.controllers = []
        self.debug = debug
        self.description = Markup(markdown(description))
        self.directory = directory
        self.functions = []
        self.host = host
        self.imports = set()
        self.init = None
        self.packages = set([])
        self.password = password
        self.port = port
        self.schedules = []
        self.subscriptions = defaultdict(list)
        self.templates = set(['progress.jsx'])
        self.title = title
        self.username = username
        self.visuals = [[]]

    def add_visual(self, visual, next_row=False):
        """Add a visual to the layout.

        Parameters
        ----------
        visual : bowtie._Visual
            A Bowtie visual instance.
        next_row : bool, optional
            Add this visual to the next row.

        """
        assert isinstance(visual, _Visual)
        # pylint: disable=protected-access
        self.packages.add(visual._PACKAGE)
        self.templates.add(visual._TEMPLATE)
        self.imports.add(_Import(component=visual._COMPONENT,
                                 module=visual._TEMPLATE[:visual._TEMPLATE.find('.')]))

        if next_row and self.visuals[-1]:
            self.visuals.append([])

        self.visuals[-1].append(visual)

    def add_controller(self, control):
        """Add a controller to the layout.

        Parameters
        ----------
        control : bowtie._Controller
            A Bowtie controller instance.

        """
        assert isinstance(control, _Controller)
        # pylint: disable=protected-access
        self.packages.add(control._PACKAGE)
        self.templates.add(control._TEMPLATE)
        self.imports.add(_Import(component=control._COMPONENT,
                                 module=control._TEMPLATE[:control._TEMPLATE.find('.')]))
        self.controllers.append(_Control(instantiate=control._instantiate,
                                         caption=control.caption))

    def subscribe(self, func, event, *events):
        """Call a function in response to an event.

        Parameters
        ----------
        func : callable
            Function to be called.
        event : event
            A Bowtie event.
        *events : Each is an event, optional
            Additional events.
        """
        all_events = [event]
        all_events.extend(events)

        for evt in all_events:
            # quoted = "'{}'".format(ev)
            self.subscriptions[evt].append((all_events, func.__name__))

    def load(self, func):
        """Call a function on load.

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

    def build(self):
        """Compiles the Bowtie application.
        """
        file_dir = path.dirname(__file__)

        env = Environment(
            loader=FileSystemLoader(path.join(file_dir, 'templates')),
            trim_blocks=True,
            lstrip_blocks=True
        )

        server = env.get_template('server.py')
        index = env.get_template('index.html')
        react = env.get_template('index.jsx')

        src, app, templates = create_directories(directory=self.directory)

        webpack_src = path.join(file_dir, 'src/webpack.config.js')
        shutil.copy(webpack_src, self.directory)

        server_path = path.join(src, server.name)
        # [1] grabs the parent stack and [1] grabs the filename
        source_filename = inspect.stack()[1][1]
        with open(server_path, 'w') as f:
            f.write(
                server.render(
                    basic_auth=self.basic_auth,
                    username=self.username,
                    password=self.password,
                    source_module=os.path.basename(source_filename)[:-3],
                    subscriptions=self.subscriptions,
                    schedules=self.schedules,
                    initial=self.init,
                    host="'{}'".format(self.host),
                    port=self.port,
                    debug=self.debug
                )
            )
        perms = os.stat(server_path)
        os.chmod(server_path, perms.st_mode | stat.S_IEXEC)

        with open(path.join(templates, index.name), 'w') as f:
            f.write(
                index.render(title=self.title)
            )

        for template in self.templates:
            template_src = path.join(file_dir, 'src', template)
            shutil.copy(template_src, app)

        for i, visualrow in enumerate(self.visuals):
            for j, visual in enumerate(visualrow):
                # pylint: disable=protected-access
                self.visuals[i][j] = visual._instantiate(), visual.progress._instantiate()

        with open(path.join(app, react.name), 'w') as f:
            f.write(
                react.render(
                    description=self.description,
                    background_color=self.background_color,
                    components=self.imports,
                    controls=self.controllers,
                    visuals=self.visuals
                )
            )

        init = Popen('yarn init -y', shell=True, cwd=self.directory).wait()
        if init != 0:
            raise YarnError('Error running "yarn init -y"')
        self.packages.discard(None)
        packages = ' '.join(self._packages + list(self.packages))
        install = Popen('yarn add {}'.format(packages),
                        shell=True, cwd=self.directory).wait()
        if install > 1:
            raise YarnError('Error install node packages')
        elif install == 1:
            print('Yarn error but trying to continue build')
        dev = Popen('webpack -d', shell=True, cwd=self.directory).wait()
        if dev != 0:
            raise WebpackError('Error building with webpack')


def create_directories(directory='build'):
    """
    Create all the necessary subdirectories for the build.
    """
    src = path.join(directory, 'src')
    templates = path.join(src, 'templates')
    app = path.join(src, 'app')
    makedirs(app, exist_ok=True)
    makedirs(templates, exist_ok=True)
    return src, app, templates
