# -*- coding: utf-8 -*-

import os
from os import path
import stat
from subprocess import Popen
import inspect

from flask import Markup

from collections import namedtuple, defaultdict

from jinja2 import Environment, FileSystemLoader
from markdown import markdown

from bowtie._compat import makedirs
from bowtie.control import _Controller
from bowtie.visual import _Visual


_Import = namedtuple('_Import', ['module', 'component'])
_Control = namedtuple('_Control', ['instantiate', 'caption'])
_Schedule = namedtuple('_Control', ['seconds', 'function'])


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
        'babel-core',
        'babel-loader',
        'babel-polyfill',
        'babel-preset-es2015',
        'babel-preset-react',
        'babel-preset-stage-0',
        'babel-plugin-transform-object-rest-spread',
        'classnames',
        'core-js',
        'css-loader',
        'extract-text-webpack-plugin',
        'less-loader',
        'lodash.clonedeep',
        'node-sass',
        'normalize.css',
        'postcss-modules-values',
        'react',
        'react-dom',
        'sass-loader',
        'socket.io-client',
        'style-loader',
        'webpack',
    ]

    def __init__(self, title='Bowtie App', description='Bowtie App\n---',
                 basic_auth=False, username='username', password='password',
                 background_color='White', directory='build',
                 host='0.0.0.0', port=9991, debug=False):
        self.title = title
        self.description = Markup(markdown(description))
        self.basic_auth = basic_auth
        self.username = username
        self.password = password
        self.background_color = background_color
        self.directory = directory
        self.host = host
        self.port = port
        self.debug = debug
        self.subscriptions = defaultdict(list)
        self.packages = set()
        self.templates = set()
        self.imports = set()
        self.visuals = [[]]
        self.controllers = []
        self.schedules = []
        self.functions = []

    def add_visual(self, visual,
                   width=None, height=None,
                   width_pixels=None, height_pixels=None,
                   next_row=False):
        """Add a visual to the layout.

        Parameters
        ----------
        visual : bowtie._Visual
            A Bowtie visual instance.
        next_row : bool, optional
            Add this visual to the next row.

        """
        assert isinstance(visual, _Visual)
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
        pass
        assert isinstance(control, _Controller)
        self.packages.add(control._PACKAGE)
        self.templates.add(control._TEMPLATE)
        self.imports.add(_Import(component=control._COMPONENT,
                                 module=control._TEMPLATE[:control._TEMPLATE.find('.')]))
        self.controllers.append(_Control(instantiate=control._instantiate,
                                         caption=control.caption))

    def subscribe(self, event, func):
        """Call a function in response to an event.

        Parameters
        ----------
        event : str
            Name of the event.
        func : callable
            Function to be called.
        """
        e = "'{}'".format(event)
        self.subscriptions[e].append(func.__name__)

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
        env = Environment(loader=FileSystemLoader(
            path.join(path.dirname(__file__), 'templates')
        ))

        webpack = env.get_template('webpack.config.js')
        server = env.get_template('server.py')
        index = env.get_template('index.html')
        react = env.get_template('index.jsx')

        src, app, templates = create_directories(directory=self.directory)

        with open(path.join(self.directory, webpack.name), 'w') as f:
            f.write(
                webpack.render()
            )

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

        # components = [env.get_template(t).render() for t in self.templates]

        for template in self.templates:
            temp = env.get_template(template)
            with open(path.join(app, temp.name), 'w') as f:
                f.write(
                    temp.render()
                )

        for i, visualrow in enumerate(self.visuals):
            for j, visual in enumerate(visualrow):
                self.visuals[i][j] = self.visuals[i][j]._instantiate()
                    # columns=len(visualrow),
                    # rows=len(self.visuals)
                # )

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

        init = Popen('npm init -f', shell=True, cwd='build').wait()
        assert init == 0, 'Error running "npm init -f"'
        packages = ' '.join(self._packages + list(self.packages))
        install = Popen('npm install -S {}'.format(packages),
                        shell=True, cwd='build').wait()
        assert install == 0, 'Error install node packages'
        dev = Popen('webpack -d', shell=True, cwd='build').wait()
        assert dev == 0, 'Error building with webpack'


def create_directories(directory='build'):
    src = path.join(directory, 'src')
    templates = path.join(src, 'templates')
    app = path.join(src, 'app')
    makedirs(app, exist_ok=True)
    makedirs(templates, exist_ok=True)
    return src, app, templates
