"""App and View testing."""
import pytest

from bowtie import App
from bowtie.control import Button


def test_subscribe_error():
    """Subscribe with incorrect argument order."""
    app = App()
    button = Button()
    with pytest.raises(TypeError):
        app.subscribe(3, button.on_click)
