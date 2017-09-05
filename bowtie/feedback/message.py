# -*- coding: utf-8 -*-
"""Messages provide a temporary message that will disappear after a few seconds.

Reference
^^^^^^^^^
https://ant.design/components/message/
"""

import flask
from flask_socketio import emit
import eventlet

from bowtie._component import pack
from bowtie._utils import func_name


def _message(status, content):
    """Send message interface.

    Parameters
    ----------
    status : str
        The type of message
    content : str

    """
    event = 'message.{}'.format(status)
    if flask.has_request_context():
        emit(event, dict(data=pack(content)))
    else:
        sio = flask.current_app.extensions['socketio']
        sio.emit(event, dict(data=pack(content)))
    eventlet.sleep()


def success(content):
    """Success message.

    Parameters
    ----------
    content : str
        Message to show user.

    """
    _message(func_name(), content)


def error(content):
    """Error message.

    Parameters
    ----------
    content : str
        Message to show user.

    """
    _message(func_name(), content)


def info(content):
    """Info message.

    Parameters
    ----------
    content : str
        Message to show user.

    """
    _message(func_name(), content)


def warning(content):
    """Warning message.

    Parameters
    ----------
    content : str
        Message to show user.

    """
    _message(func_name(), content)


def loading(content):
    """Load message.

    Parameters
    ----------
    content : str
        Message to show user.

    """
    _message(func_name(), content)
