"""Utility functions for testing only."""

from contextlib import contextmanager
from multiprocessing import Process
import time

from bowtie import View
from bowtie._component import Component


def reset_uuid():
    """Reset the uuid counter for components."""
    # pylint: disable=protected-access
    Component._NEXT_UUID = 0
    View._NEXT_UUID = 0


@contextmanager
def server_check(app):
    """Context manager for testing Bowtie apps and verifying no errors happened."""
    process = Process(target=app._serve)  # pylint: disable=protected-access
    process.start()
    time.sleep(5)
    yield process
    process.terminate()
