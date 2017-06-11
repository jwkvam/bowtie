# -*- coding: utf-8 -*-
"""Bowtie abstract component classes.

All visual and control components inherit these.
"""

# need this for get commands on python2
from __future__ import unicode_literals

# pylint: disable=redefined-builtin
from builtins import bytes

import string
import inspect
from functools import wraps
import json
from datetime import datetime, date, time

import msgpack
import flask
from flask_socketio import emit
from future.utils import with_metaclass
import eventlet
from eventlet.queue import LightQueue


def varname(variable):
    """Return the name of the given variable."""
    frame = inspect.stack()[2][0]
    for name, var in frame.f_locals.items():
        if variable is var:
            return name
    for name, var in frame.f_globals.items():
        if variable is var:
            return name


def jsbool(x):
    """Convert Python bool to Javascript bool."""
    return repr(x).lower()


def json_conversion(obj):
    """Encode additional objects to JSON."""
    try:
        # numpy isn't an explicit dependency of bowtie
        # so we can't assume it's available
        import numpy as np
        if isinstance(obj, (np.ndarray, np.generic)):
            return obj.tolist()
    except ImportError:
        pass

    try:
        # pandas isn't an explicit dependency of bowtie
        # so we can't assume it's available
        import pandas as pd
        if isinstance(obj, pd.Index):
            return obj.tolist()
    except ImportError:
        pass

    if isinstance(obj, (datetime, time, date)):
        return obj.isoformat()
    raise TypeError('Not sure how to serialize {} of type {}'.format(obj, type(obj)))


def jdumps(data):
    """Encode Python object to JSON with additional encoders."""
    return json.dumps(data, default=json_conversion)


def encoders(obj):
    """Convert Python object to msgpack encodable ones."""
    try:
        # numpy isn't an explicit dependency of bowtie
        # so we can't assume it's available
        import numpy as np
        if isinstance(obj, (np.ndarray, np.generic)):
            # https://docs.scipy.org/doc/numpy/reference/arrays.scalars.html
            return obj.tolist()
    except ImportError:
        pass

    try:
        # pandas isn't an explicit dependency of bowtie
        # so we can't assume it's available
        import pandas as pd
        if isinstance(obj, pd.Index):
            return obj.tolist()
    except ImportError:
        pass

    if isinstance(obj, (datetime, time, date)):
        return obj.isoformat()

    return obj


def pack(x):
    """Encode ``x`` into msgpack with additional encoders."""
    return bytes(msgpack.packb(x, default=encoders))


def unpack(x):
    """Decode ``x`` from msgpack into Python object."""
    return msgpack.unpackb(bytes(x['data']), encoding='utf8')


def make_event(event):
    """Create an event from a method signature."""
    # pylint: disable=missing-docstring
    @property
    @wraps(event)
    def actualevent(self):
        name = event.__name__[3:]
        # pylint: disable=protected-access
        ename = '{uuid}#{event}'.format(uuid=self._uuid, event=name)
        objname = varname(self)
        try:
            # the getter post processing function
            # is preserved with an underscore
            getter = event(self).__name__
        except AttributeError:
            getter = None
        return ename, objname, getter

    return actualevent


def is_event(attribute):
    """Test if a method is an event."""
    return attribute.startswith('on_')


def make_command(command):
    """Create an command from a method signature."""
    # pylint: disable=missing-docstring
    @wraps(command)
    def actualcommand(self, *args, **kwds):
        data = command(self, *args, **kwds)
        name = command.__name__[3:]
        # pylint: disable=protected-access
        signal = '{uuid}#{event}'.format(uuid=self._uuid, event=name)
        if flask.has_request_context():
            emit(signal, {'data': pack(data)})
        else:
            sio = flask.current_app.extensions['socketio']
            sio.emit(signal, {'data': pack(data)})
        eventlet.sleep()

    return actualcommand


def is_command(attribute):
    """Test if a method is an command."""
    return attribute.startswith('do_')


def make_getter(getter):
    """Create an command from a method signature."""
    # pylint: disable=missing-docstring
    def get(self, timeout=10):
        name = getter.__name__
        # pylint: disable=protected-access
        signal = '{uuid}#{event}'.format(uuid=self._uuid, event=name)
        event = LightQueue(1)
        if flask.has_request_context():
            emit(signal, callback=lambda x: event.put(unpack(x)))
        else:
            sio = flask.current_app.extensions['socketio']
            sio.emit(signal, callback=lambda x: event.put(unpack(x)))
        data = event.get(timeout=timeout)
        return getter(self, data)

    # don't want to copy the signature in this case
    get.__doc__ = getter.__doc__

    return get


def is_getter(attribute):
    """Test if a method is a getter.

    It can be `get` or `get_*`.
    """
    return attribute.startswith('get')


class _Maker(type):
    def __new__(mcs, name, parents, dct):
        for k in list(dct.keys()):
            if is_event(k):
                dct[k] = make_event(dct[k])
            if is_command(k):
                dct[k] = make_command(dct[k])
            if is_getter(k):
                # preserve the post-processor with an underscore
                dct['_' + k] = dct[k]
                dct[k] = make_getter(dct[k])
        return super(_Maker, mcs).__new__(mcs, name, parents, dct)


class FormatDict(dict):
    """Dict to replace missing keys."""

    def __missing__(self, key):
        """Replace missing key with "{key"}"."""
        return "{" + key + "}"


# pylint: disable=too-few-public-methods
class Component(with_metaclass(_Maker, object)):
    """Abstract class for all components.

    All visual and control classes subclass this so their events
    and commands get transformed by the metaclass.
    """

    _NEXT_UUID = 0

    @classmethod
    def _next_uuid(cls):
        cls._NEXT_UUID += 1
        return cls._NEXT_UUID

    def __init__(self):
        """Give the component a unique ID."""
        # wanted to put "self" instead of "Component"
        # was surprised that didn't work
        self._uuid = Component._next_uuid()
        super(Component, self).__init__()
        self._tagbase = " socket={{socket}} uuid={{'{uuid}'}} />".format(uuid=self._uuid)
        self._tag = '<' + self._COMPONENT
        if self._ATTRS:
            self._tag += ' ' + self._ATTRS

    @staticmethod
    def _insert(wrap, tag):
        """Insert the component tag into the wrapper html.

        This ignores other tags already created like ``{socket}``.

        https://stackoverflow.com/a/11284026/744520
        """
        formatter = string.Formatter()
        mapping = FormatDict(component=tag)
        return formatter.vformat(wrap, (), mapping)
