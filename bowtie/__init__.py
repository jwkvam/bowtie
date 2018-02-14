"""Interactive Dashboard Toolkit."""

__version__ = '0.8.1'

from bowtie._app import App, View
from bowtie._command import command
from bowtie.pager import Pager
from bowtie._cache import cache


def load_ipython_extension(ip):
    """ API for IPython to recognize this module as an IPython extension.
    """
    from bowtie._magic import BowtieMagic
    ip.register_magics(BowtieMagic)
