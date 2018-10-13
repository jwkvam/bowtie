"""Jupyter Integration."""

import ast
import socket
from os.path import join as pjoin
from urllib.parse import urljoin
import json
import re
import sys
import types
import time
from multiprocessing import Process

from IPython import get_ipython
from IPython.display import display, HTML, clear_output
from IPython.core.error import UsageError
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import Magics, magics_class, line_magic
from nbformat import read
from notebook.notebookapp import list_running_servers
import ipykernel
import requests

from bowtie._app import App


def get_notebook_name() -> str:
    """Return the full path of the jupyter notebook.

    References
    ----------
    https://github.com/jupyter/notebook/issues/1000#issuecomment-359875246

    """
    kernel_id = re.search(  # type: ignore
        'kernel-(.*).json',
        ipykernel.connect.get_connection_file()
    ).group(1)
    servers = list_running_servers()
    for server in servers:
        response = requests.get(urljoin(server['url'], 'api/sessions'),
                                params={'token': server.get('token', '')})
        for session in json.loads(response.text):
            if session['kernel']['id'] == kernel_id:
                relative_path = session['notebook']['path']
                return pjoin(server['notebook_dir'], relative_path)
    raise Exception('Noteboook not found.')


def load_notebook(fullname: str):
    """Import a notebook as a module."""
    shell = InteractiveShell.instance()
    path = fullname

    # load the notebook object
    with open(path, 'r', encoding='utf-8') as f:
        notebook = read(f, 4)

    # create the module and add it to sys.modules
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
                try:
                    # only run valid python code
                    ast.parse(cell.source)
                except SyntaxError:
                    continue
                try:
                    # pylint: disable=exec-used
                    exec(cell.source, mod.__dict__)
                except NameError:
                    print(cell.source)
                    raise
    finally:
        shell.user_ns = save_user_ns
    return mod


@magics_class
class BowtieMagic(Magics):
    """Bowtie magic commands."""

    process = None

    @line_magic
    def bowtie_stop(self, line=''):  # pylint: disable=unused-argument
        """Terminate Bowtie app."""
        if self.process is None:
            print('No app has been run.')
        else:
            print('Terminating Bowtie app.')
            self.process.terminate()
            if self.process.is_alive():
                time.sleep(1)
                self.process.kill()
                time.sleep(1)
                if self.process.is_alive():
                    print('Failed to stop Bowtie app.', file=sys.stderr)
                    return
            print('Successfully stopped Bowtie app.')
            self.process.close()
            self.process = None

    @line_magic
    def bowtie(self, line=''):
        """Build and serve a Bowtie app."""
        opts, appvar = self.parse_options(line, 'w:h:b:p:')
        width = opts.get('w', 1500)
        height = opts.get('h', 1000)
        border = opts.get('b', 2)
        port = opts.get('p', 9991)
        host = '0.0.0.0'

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        if result == 0:
            raise Exception(f'Port {port} is unavailable on host {host}, aborting.')

        global_ns = self.shell.user_global_ns
        local_ns = self.shell.user_ns
        try:
            # pylint: disable=eval-used
            app = eval(appvar, global_ns, local_ns)
        except NameError:
            raise UsageError(f'Could not find App {appvar}')

        if not isinstance(app, App):
            raise UsageError(f'App is of type {type(app)} needs to be type <bowtie.App>')

        app._build(notebook=get_notebook_name())  # pylint: disable=protected-access
        self.process = Process(target=app._serve)  # pylint: disable=protected-access
        self.process.start()
        time.sleep(5)

        clear_output()
        display(HTML(
            f'<iframe src=http://localhost:9991 width={width} height={height} '
            f'frameBorder={border}></iframe>'
        ))
