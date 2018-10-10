"""App and View testing."""
import pytest

from bowtie import App
from bowtie.control import Button


def test_subscribe_error():
    """Subscribe with incorrect argument order."""
    app = App()
    with pytest.raises(IndexError):
        app.subscribe()
