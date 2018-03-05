"""Interactive Dashboard Toolkit."""

__version__ = '0.9.2-dev'

from bowtie._app import App, View
from bowtie._command import command
from bowtie.pager import Pager
from bowtie._cache import cache


def load_ipython_extension(ipython):
    """Enable IPython extension."""
    from bowtie._magic import BowtieMagic
    ipython.register_magics(BowtieMagic)
