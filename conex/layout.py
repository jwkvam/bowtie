# -*- coding: utf-8 -*-

import os
from os import path
import stat
from subprocess import Popen

import dill as pickle

from jinja2 import Environment, FileSystemLoader

from conex.compat import makedirs


class _Subscription(object):

    def __init__(self, event, func):
        self.event = event
        self.func = pickle.dumps(func)


class Layout(object):

    def __init__(self, title=None):
        self.title = title
        self.subscriptions = []

    def add_visual(self, visual):
        pass

    def add_control(self, control):
        pass

    def subscribe(self, event, func):
        sub = _Subscription(event, func)
        self.subscriptions.append(sub)
        # socket.on('{name}#{event}'.format(self.name, event))(func)

    def build(self, directory='build', host='0.0.0.0', port=9991,
              debug=False):
        env = Environment(loader=FileSystemLoader(
            path.join(path.dirname(__file__), 'templates')
        ))

        package = env.get_template('package.json')
        webpack = env.get_template('webpack.config.js')
        server = env.get_template('server.py')
        index = env.get_template('index.html')
        react = env.get_template('index.jsx')

        src, app, templates = create_directories(directory=directory)

        with open(path.join(directory, package.name), 'w') as f:
            f.write(
                package.render()
            )

        with open(path.join(directory, webpack.name), 'w') as f:
            f.write(
                webpack.render()
            )

        server_path = path.join(src, server.name)
        with open(server_path, 'w') as f:
            f.write(
                server.render(
                    subscriptions=self.subscriptions,
                    host="'{}'".format(host),
                    port=port,
                    debug=debug
                )
            )
        perms = os.stat(server_path)
        os.chmod(server_path, perms.st_mode | stat.S_IEXEC)

        with open(path.join(templates, index.name), 'w') as f:
            f.write(
                index.render(title=self.title)
            )

        with open(path.join(app, react.name), 'w') as f:
            f.write(
                react.render(title=self.title)
            )

        install = Popen('npm install', shell=True, cwd='build')
        install.wait()
        dev = Popen('npm run dev', shell=True, cwd='build')
        dev.wait()


def create_directories(directory='build'):
    src = path.join(directory, 'src')
    templates = path.join(src, 'templates')
    app = path.join(src, 'app')
    makedirs(app, exist_ok=True)
    makedirs(templates, exist_ok=True)
    return src, app, templates
