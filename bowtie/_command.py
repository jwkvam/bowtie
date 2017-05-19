# -*- coding: utf-8 -*-
"""
Decorates a function for Bowtie.

Reference
---------
https://gist.github.com/carlsmith/800cbe3e11f630ac8aa0
"""

import sys
import inspect
from subprocess import call

import click

from bowtie._compat import numargs


class WrongNumberOfArguments(TypeError):
    """The "build" function accepts an incorrect number of arguments."""

    pass


def command(func):
    """Command line interface decorator.

    Decorate a function for building a Bowtie
    application and turn it into a command line interface.
    """
    @click.group(options_metavar='[-p <path>] [--help]')
    @click.option('--path', '-p', default='build', type=str,
                  help='Path to build the app.')
    @click.pass_context
    def cmd(ctx, path):
        """Bowtie CLI to help build and run your app."""
        ctx.obj = path

    # pylint: disable=unused-variable
    @cmd.command(add_help_option=False)
    @click.pass_context
    def build(ctx):
        """Write the app, downloads the packages, and bundles it with Webpack."""
        nargs = numargs(func)
        if nargs == 0:
            func()
        elif nargs == 1:
            func(ctx.obj)
        else:
            raise WrongNumberOfArguments(
                'Function "{}" should have 0 or 1 argument, it has {}.'
                .format(func.__name__, nargs)
            )

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def serve(ctx, extra):
        """Serve the Bowtie app."""
        line = ('./{}/src/server.py'.format(ctx.obj),) + extra
        call(line)

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def dev(ctx, extra):
        """Recompile the app for development."""
        line = ('webpack', '-d') + extra
        call(line, cwd=ctx.obj)

    @cmd.command(context_settings=dict(ignore_unknown_options=True),
                 add_help_option=False)
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def prod(ctx, extra):
        """Recompile the app for production."""
        line = ('webpack', '--define', 'process.env.NODE_ENV="production"', '--progress') + extra
        call(line, cwd=ctx.obj)

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
