"""Interactive Dashboard Toolkit."""

__version__ = '0.8.1'

from bowtie._app import App, View
from bowtie._command import command
from bowtie.pager import Pager
from bowtie._cache import cache


def load_ipython_extension(ipython):
    """Enable IPython extension."""
    import sys
    if sys.version_info < (3,):
        raise Exception('Bowtie magics only support Python 3.')
    from bowtie._magic import BowtieMagic
    ipython.register_magics(BowtieMagic)
