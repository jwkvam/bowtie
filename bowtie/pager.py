"""Bowtie pager."""

import flask
from flask_socketio import emit
import eventlet

from bowtie._component import SEPARATOR

_NAME = 'page' + SEPARATOR


class Pager:
    """Tell the client to send a message to the server."""

    _NEXT_UUID = 0

    @classmethod
    def _next_uuid(cls):
        cls._NEXT_UUID += 1
        return cls._NEXT_UUID

    def __init__(self):
        """Create a pager."""
        self._uuid = Pager._next_uuid()

    def notify(self):
        """Notify the client.

        The function passed to ``App.respond`` will get called.
        """
        if flask.has_request_context():
            emit(_NAME + str(self._uuid))
        else:
            sio = flask.current_app.extensions['socketio']
            sio.emit(_NAME + str(self._uuid))
        eventlet.sleep()
