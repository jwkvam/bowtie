# -*- coding: utf-8 -*-
"""
Decorates a function for Bowtie.

Reference
---------
https://gist.github.com/carlsmith/800cbe3e11f630ac8aa0
"""

from __future__ import print_function

import os
import sys
import inspect
from subprocess import call

import click

from bowtie._compat import numargs
from bowtie._app import _DIRECTORY


class WrongNumberOfArguments(TypeError):
    """The "build" function accepts an incorrect number of arguments."""

    pass


def command(func):
    """Command line interface decorator.

    Decorate a function for building a Bowtie
    application and turn it into a command line interface.
    """
    @click.group(options_metavar='[--help]')
    @click.pass_context
    def cmd(ctx):
        """Bowtie CLI to help build and run your app."""
        pass

    # pylint: disable=unused-variable
    @cmd.command(add_help_option=False)
    @click.pass_context
    def build(ctx):
        """Write the app, downloads the packages, and bundles it with Webpack."""
        nargs = numargs(func)
        if nargs == 0:
            app = func()
        else:
            raise WrongNumberOfArguments(
                'Decorated function "{}" should have no arguments, it has {}.'
                .format(func.__name__, nargs)
            )
        print('building')
        app._build()

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def run(ctx, extra):
        """Write the app, downloads the packages, and bundles it with Webpack."""
        nargs = numargs(func)
        if nargs == 0:
            app = func()
        else:
            raise WrongNumberOfArguments(
                'Decorated function "{}" should have no arguments, it has {}.'
                .format(func.__name__, nargs)
            )
        print('running')
        app._write_templates()
        app._translate()
        # filepath = './{}/src/server.py'.format(_DIRECTORY)
        # line = (filepath,) + extra
        # call(line)

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def serve(ctx, extra):
        """Serve the Bowtie app."""
        filepath = './{}/src/server.py'.format(_DIRECTORY)
        if os.path.isfile(filepath):
            line = (filepath,) + extra
            call(line)
        else:
            print("Cannot find '{}'. Did you build the app?".format(filepath))

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def dev(ctx, extra):
        """Recompile the app for development."""
        line = ('webpack', '-d') + extra
        call(line, cwd=_DIRECTORY)

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def prod(ctx, extra):
        """Recompile the app for production."""
        line = ('webpack', '--define', 'process.env.NODE_ENV="production"', '--progress') + extra
        call(line, cwd=_DIRECTORY)

    locale = inspect.stack()[1][0].f_locals
    module = locale.get("__name__")

    if module == "__main__":
        try:
            arg = sys.argv[1:]
        except IndexError:
            arg = ('--help',)
        # pylint: disable=no-value-for-parameter
        sys.exit(cmd(arg))

    return cmd
