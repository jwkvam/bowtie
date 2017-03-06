# -*- coding: utf-8 -*-
"""
Bowtie cache functions
"""

import flask
from flask_socketio import emit
import eventlet
from eventlet.queue import LightQueue

from bowtie._component import pack, unpack


def save(key, value):
    """Stores the key value pair.

    Parameters
    ----------
    key : object
    value : object

    Returns
    -------
    None

    """
    signal = 'cache_save'
    if flask.has_request_context():
        emit(signal, {'data': pack((key, value))})
    else:
        sio = flask.current_app.extensions['socketio']
        sio.emit(signal, {'data': pack((key, value))})
    eventlet.sleep()


def load(key):
    """Loads the value stored with the key.

    Parameters
    ----------
    key : object

    Returns
    -------
    The value if the key exists, otherwise None.

    """
    signal = 'cache_load'
    event = LightQueue(1)
    if flask.has_request_context():
        emit(signal, {'data': pack(key)}, callback=lambda x: event.put(unpack(x)))
    else:
        sio = flask.current_app.extensions['socketio']
        sio.emit(signal, {'data': pack(key)}, callback=lambda x: event.put(unpack(x)))
    return event.get(timeout=10)
