# -*- coding: utf-8 -*-
"""Bowtie cache functions."""

import flask
from flask_socketio import emit
import eventlet
from eventlet.queue import LightQueue
import msgpack

from bowtie._component import pack


def save(key, value):
    """Store the key value pair.

    Parameters
    ----------
    key : object
        The key to determine where it's stored, you'll need this to load the value later.
    value : object
        The value to store in the cache.

    Returns
    -------
    None

    """
    signal = 'cache_save'
    if flask.has_request_context():
        emit(signal, {'key': pack(key), 'data': pack(value)})
    else:
        sio = flask.current_app.extensions['socketio']
        sio.emit(signal, {'key': pack(key), 'data': pack(value)})
    eventlet.sleep()


def load(key):
    """Load the value stored with the key.

    Parameters
    ----------
    key : object
        The key to lookup the value stored.

    Returns
    -------
    object
        The value if the key exists in the cache, otherwise None.

    """
    signal = 'cache_load'
    event = LightQueue(1)
    if flask.has_request_context():
        emit(signal, {'data': pack(key)}, callback=event.put)
    else:
        sio = flask.current_app.extensions['socketio']
        sio.emit(signal, {'data': pack(key)}, callback=event.put)
    return msgpack.unpackb(bytes(event.get(timeout=10)), encoding='utf8')
