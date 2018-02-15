# -*- coding: utf-8 -*-
"""Jupyter Integration."""


import os
from os.path import join as pjoin
from urllib.parse import urljoin
import json
import re
import sys
import types
from subprocess import Popen, PIPE, STDOUT

from IPython import get_ipython, display
from IPython.core.error import UsageError
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import Magics, magics_class, line_magic
from nbformat import read
from notebook.notebookapp import list_running_servers
import ipykernel
import requests

from bowtie._app import _DIRECTORY, App


def get_notebook_name():
    """Return the full path of the jupyter notebook.

    References
    ----------
    https://github.com/jupyter/notebook/issues/1000#issuecomment-359875246

    """
    kernel_id = re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for server in servers:
        response = requests.get(urljoin(server['url'], 'api/sessions'),
                                params={'token': server.get('token', '')})
        for session in json.loads(response.text):
            if session['kernel']['id'] == kernel_id:
                relative_path = session['notebook']['path']
                return pjoin(server['notebook_dir'], relative_path)
    raise Exception('Noteboook not found.')


def load_notebook(fullname):
    """Import a notebook as a module."""
    shell = InteractiveShell.instance()
    path = fullname

    # load the notebook object
    with open(path, 'r', encoding='utf-8') as f:
        notebook = read(f, 4)

    # create the module and add it to sys.modules
    # if name in sys.modules:
    #    return sys.modules[name]
    mod = types.ModuleType(fullname)
    mod.__file__ = path
    # mod.__loader__ = self
    mod.__dict__['get_ipython'] = get_ipython
    sys.modules[fullname] = mod

    # extra work to ensure that magics that would affect the user_ns
    # actually affect the notebook module's ns
    save_user_ns = shell.user_ns
    shell.user_ns = mod.__dict__

    try:
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                # transform the input to executable Python
                code = shell.input_transformer_manager.transform_cell(cell.source)
                # run the code in the module
                try:
                    # pylint: disable=exec-used
                    exec(code, mod.__dict__)
                except SyntaxError:
                    print('Could not exec: "{}"'.format(code))
    finally:
        shell.user_ns = save_user_ns
    return mod


@magics_class
class BowtieMagic(Magics):
    """Bowtie magic commands."""

    @line_magic
    def bowtie(self, appvar=''):
        """Build and serve a Bowtie app."""
        width = 1500
        height = 1000
        global_ns = self.shell.user_global_ns
        local_ns = self.shell.user_ns
        try:
            # pylint: disable=eval-used
            app = eval(appvar, global_ns, local_ns)
        except NameError:
            raise UsageError('Could not find App {}'.format(appvar))

        if not isinstance(app, App):
            raise UsageError('App is of type {} needs to be type <bowtie.App>'.format(type(app)))

        # pylint: disable=protected-access
        app._build(notebook=get_notebook_name())

        filepath = './{}/src/server.py'.format(_DIRECTORY)
        if os.path.isfile(filepath):
            server = Popen(['python', '-u', filepath], stdout=PIPE, stderr=STDOUT)
        else:
            print('Cannot find "{}". Did you build the app?'.format(filepath))

        display.HTML(
            '<iframe src=http://localhost:9991 width={} height={} '
            'frameBorder=0></iframe>'.format(width, height)
        )
        return server
