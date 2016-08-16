# -*- coding: utf-8 -*-

import os
from os import path
import stat
from subprocess import Popen
import inspect

from collections import namedtuple, defaultdict

from jinja2 import Environment, FileSystemLoader

from bowtie.compat import makedirs
from bowtie.control import Controller
from bowtie.visual import Visual


_Import = namedtuple('_Import', ['module', 'component'])
_Control = namedtuple('_Control', ['instantiate', 'caption'])


class Layout(object):

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

    def __init__(self, title=None):
        self.title = title
        self.subscriptions = defaultdict(list)
        self.packages = set()
        self.templates = set()
        self.imports = set()
        self.visuals = [[]]
        self.controllers = []
        self.functions = []

    def add_visual(self, visual,
                   width=None, height=None,
                   width_pixels=None, height_pixels=None,
                   next_row=False):
        assert isinstance(visual, Visual)
        self.packages.add(visual.package)
        self.templates.add(visual.template)
        self.imports.add(_Import(component=visual.component,
                                 module=visual.template[:visual.template.find('.')]))

        if next_row and self.visuals[-1]:
            self.visuals.append([])

        self.visuals[-1].append(visual)

    def add_controller(self, control):
        assert isinstance(control, Controller)
        self.packages.add(control.package)
        self.templates.add(control.template)
        self.imports.add(_Import(component=control.component,
                                 module=control.template[:control.template.find('.')]))
        self.controllers.append(_Control(instantiate=control.instantiate,
                                         caption=control.caption))

    def subscribe(self, event, func):
        e = "'{}'".format(event)
        self.subscriptions[e].append(func.__name__)


    def build(self, directory='build', host='0.0.0.0', port=9991,
              debug=False):

        env = Environment(loader=FileSystemLoader(
            path.join(path.dirname(__file__), 'templates')
        ))

        webpack = env.get_template('webpack.config.js')
        server = env.get_template('server.py')
        index = env.get_template('index.html')
        react = env.get_template('index.jsx')

        src, app, templates = create_directories(directory=directory)

        with open(path.join(directory, webpack.name), 'w') as f:
            f.write(
                webpack.render()
            )

        server_path = path.join(src, server.name)
        # [1] grabs the parent stack and [1] grabs the filename
        source_filename = inspect.stack()[1][1]
        with open(server_path, 'w') as f:
            print('writing server')
            f.write(
                server.render(
                    source_module=os.path.basename(source_filename)[:-3],
                    subscriptions=self.subscriptions,
                    host="'{}'".format(host),
                    port=port,
                    debug=debug
                )
            )
            print('done writing server')
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
                self.visuals[i][j] = self.visuals[i][j].instantiate(
                    columns=len(visualrow),
                    rows=len(self.visuals)
                )

        with open(path.join(app, react.name), 'w') as f:
            f.write(
                react.render(
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
