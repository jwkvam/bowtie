# -*- coding: utf-8 -*-
"""Jupyter Integration"""


import os
import sys
import types
import json
from os.path import join as pjoin
import re
from urllib.parse import urljoin
from subprocess import Popen, PIPE, STDOUT

import ipykernel
import requests
from IPython import get_ipython, display
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.page import page
from IPython.utils.ipstruct import Struct
from IPython.core.error import UsageError
from notebook.notebookapp import list_running_servers
from nbformat import read

from bowtie import App
from bowtie._app import _DIRECTORY


def get_notebook_name():
    """Return the full path of the jupyter notebook.

    References
    ----------
    https://github.com/jupyter/notebook/issues/1000#issuecomment-359875246
    """
    kernel_id = re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return pjoin(ss['notebook_dir'], relative_path)


def load_notebook(fullname):
    """import a notebook as a module"""
    shell = InteractiveShell.instance()
    path = fullname

    # load the notebook object
    with open(path, 'r', encoding='utf-8') as f:
        nb = read(f, 4)

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
        for cell in nb.cells:
            if cell.cell_type == 'code':
                # transform the input to executable Python
                code = shell.input_transformer_manager.transform_cell(cell.source)
                # run the code in themodule
                try:
                    exec(code, mod.__dict__)
                except Exception:
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
        global_ns = self.shell.user_global_ns
        local_ns = self.shell.user_ns
        try:
            app = eval(appvar, global_ns, local_ns)
        except Exception:
            raise UsageError('Could not find App {}'.format(appvar))

        if not isinstance(app, App):
            raise UsageError('App is of type {} needs to be type bowtie.App'.format(type(app)))

        # pylint: disable=protected-access
        app._build(notebook=get_notebook_name())

        filepath = './{}/src/server.py'.format(_DIRECTORY)
        if os.path.isfile(filepath):
            server = Popen(filepath)
        else:
            print("Cannot find '{}'. Did you build the app?".format(filepath))

        display.HTML(
            '<iframe src=http://localhost:9991 width={} height={} '
            'frameBorder=0></iframe>'.format(width, height)
        )
        return server
