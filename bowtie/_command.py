"""
Decorates a function for Bowtie.

Reference
---------
https://gist.github.com/carlsmith/800cbe3e11f630ac8aa0
"""

from typing import Callable
import sys
import inspect
from subprocess import call

import click

from bowtie._app import _WEBPACK, App


class WrongNumberOfArguments(TypeError):
    """The "build" function accepts an incorrect number of arguments."""


def numargs(func: Callable) -> int:
    """Get number of arguments."""
    return len(inspect.signature(func).parameters)


def command(func):
    """Command line interface decorator.

    Decorate a function for building a Bowtie
    application and turn it into a command line interface.
    """
    # pylint: disable=protected-access,unused-variable
    nargs = numargs(func)
    if nargs > 0:
        raise WrongNumberOfArguments(
            f'Decorated function "{func.__name__}" should have no arguments, it has {nargs}.'
        )
    app = func()
    if app is None:
        raise TypeError(
            'No `App` instance was returned. '
            'In the function decorated with @command, '
            'return the `App` instance so it can be built.'
        )
    if not isinstance(app, App):
        raise TypeError(
            f'Returned value {app} is of type {type(app)}, '
            'it needs to be a bowtie.App instance.'
        )

    @click.group(options_metavar='[--help]')
    def cmd():
        """Bowtie CLI to help build and run your app."""

    @cmd.command(add_help_option=False)
    def build():
        """Write the app, downloads the packages, and bundles it with Webpack."""
        app._build()

    @cmd.command(add_help_option=False)
    @click.option('--host', '-h', default='0.0.0.0', type=str)
    @click.option('--port', '-p', default=9991, type=int)
    def run(host, port):
        """Build the app and serve it."""
        app._build()
        app._serve(host, port)

    @cmd.command(add_help_option=True)
    @click.option('--host', '-h', default='0.0.0.0', type=str)
    @click.option('--port', '-p', default=9991, type=int)
    def serve(host, port):
        """Serve the Bowtie app."""
        app._serve(host, port)

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    def dev(extra):
        """Recompile the app for development."""
        line = (_WEBPACK, '--config', 'webpack.dev.js') + extra
        call(line, cwd=app._build_dir)

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    def prod(extra):
        """Recompile the app for production."""
        line = (_WEBPACK, '--config', 'webpack.prod.js', '--progress') + extra
        call(line, cwd=app._build_dir)

    locale = inspect.stack()[1][0].f_locals
    module = locale.get("__name__")

    if module == "__main__":
        try:
            arg = sys.argv[1:]
        except IndexError:
            arg = ('--help',)
        # pylint: disable=too-many-function-args
        sys.exit(cmd(arg))

    return cmd
