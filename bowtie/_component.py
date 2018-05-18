# -*- coding: utf-8 -*-
"""Bowtie abstract component classes.

All visual and control components inherit these.
"""

from typing import Any, Callable, Optional, ClassVar, Tuple  # pylint: disable=unused-import
from abc import ABCMeta, abstractmethod
import string
from functools import wraps
import json
from datetime import datetime, date, time

import msgpack
import flask
from flask_socketio import emit
import eventlet
from eventlet.queue import LightQueue

from bowtie.exceptions import SerializationError
from bowtie._typing import JSON


COMPONENT_REGISTRY = {}
SEPARATOR = '#'


class Event:
    """Data structure to hold information for events."""

    def __init__(self, name: str, uuid: int, getter: Optional[str] = None) -> None:
        """Create an event.

        Parameters
        ----------
        name : str
        uuid : int
        getter : str, optional

        """
        self.name = name
        self.uuid = uuid
        self.getter = getter

    @property
    def signal(self) -> str:
        """Name of socket.io message."""
        return '{}{}{}'.format(self.uuid, SEPARATOR, self.name)

    @property
    def _key(self) -> Tuple[str, int, Optional[str]]:
        return self.name, self.uuid, self.getter

    def __repr__(self) -> str:
        """Create an Event."""
        return "Event('{}', {}, '{}')".format(self.name, self.uuid, self.getter)

    def __eq__(self, other) -> bool:
        """Compare Events for equality."""
        # pylint: disable=protected-access
        return isinstance(other, type(self)) and self._key == other._key

    def __hash__(self) -> int:
        """Compute hash for Event."""
        return hash(self._key)


def jsbool(x: bool) -> str:
    """Convert Python bool to Javascript bool."""
    return repr(x).lower()


def json_conversion(obj: Any) -> JSON:
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
        if isinstance(obj, pd.DatetimeIndex):
            return [x.isoformat() for x in obj.to_pydatetime()]
        if isinstance(obj, pd.Index):
            return obj.tolist()
        if isinstance(obj, pd.Series):
            try:
                return [x.isoformat() for x in obj.dt.to_pydatetime()]
            except AttributeError:
                return obj.tolist()
    except ImportError:
        pass

    if isinstance(obj, (datetime, time, date)):
        return obj.isoformat()
    raise TypeError('Not sure how to serialize {} of type {}'.format(obj, type(obj)))


def jdumps(data: Any) -> str:
    """Encode Python object to JSON with additional encoders."""
    return json.dumps(data, default=json_conversion)


def encoders(obj: Any) -> JSON:  # pylint: disable=too-many-return-statements
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
        if isinstance(obj, pd.DatetimeIndex):
            return [x.isoformat() for x in obj.to_pydatetime()]
        if isinstance(obj, pd.Index):
            return obj.tolist()
        if isinstance(obj, pd.Series):
            try:
                return [x.isoformat() for x in obj.dt.to_pydatetime()]
            except AttributeError:
                return obj.tolist()
    except ImportError:
        pass

    if isinstance(obj, (datetime, time, date)):
        return obj.isoformat()

    return obj


def pack(x: Any) -> bytes:
    """Encode ``x`` into msgpack with additional encoders."""
    try:
        return msgpack.packb(x, default=encoders)
    except TypeError as exc:
        message = ('Serialization error, check the data passed to a do_ command. '
                   'Cannot serialize this object:\n') + str(exc)[16:]
        raise SerializationError(message)


def unpack(x) -> JSON:
    """Decode ``x`` from msgpack into Python object."""
    return msgpack.unpackb(x, encoding='utf8')


def make_event(event: Callable) -> Callable:
    """Create an event from a method signature."""
    @property  # type: ignore
    @wraps(event)
    def actualevent(self):  # pylint: disable=missing-docstring
        name = event.__name__[3:]
        try:
            # the getter post processing function
            # is preserved with an underscore
            getter = event(self).__name__
        except AttributeError:
            getter = None
        return Event(name, self._uuid, getter)  # pylint: disable=protected-access

    return actualevent


def is_event(attribute: str) -> bool:
    """Test if a method is an event."""
    return attribute.startswith('on_')


def make_command(command: Callable) -> Callable:
    """Create an command from a method signature."""
    @wraps(command)
    def actualcommand(self, *args, **kwds):  # pylint: disable=missing-docstring
        data = command(self, *args, **kwds)
        name = command.__name__[3:]
        signal = '{uuid}{sep}{event}'.format(
            uuid=self._uuid,  # pylint: disable=protected-access
            sep=SEPARATOR,
            event=name
        )
        if flask.has_request_context():
            emit(signal, {'data': pack(data)})
        else:
            sio = flask.current_app.extensions['socketio']
            sio.emit(signal, {'data': pack(data)})
        eventlet.sleep()

    return actualcommand


def is_command(attribute: str) -> bool:
    """Test if a method is an command."""
    return attribute.startswith('do_')


def make_getter(getter: Callable) -> Callable:
    """Create an command from a method signature."""
    def get(self, timeout=10):  # pylint: disable=missing-docstring
        name = getter.__name__
        signal = '{uuid}{sep}{event}'.format(
            uuid=self._uuid,  # pylint: disable=protected-access
            sep=SEPARATOR,
            event=name
        )
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


def is_getter(attribute: str) -> bool:
    """Test if a method is a getter.

    It can be `get` or `get_*`.
    """
    return attribute.startswith('get')


class _Maker(ABCMeta):
    def __new__(mcs, name, bases, namespace):  # pylint: disable=arguments-differ
        for k in list(namespace.keys()):
            if is_event(k):
                namespace[k] = make_event(namespace[k])
            if is_command(k):
                namespace[k] = make_command(namespace[k])
            if is_getter(k):
                # preserve the post-processor with an underscore
                namespace['_' + k] = namespace[k]
                namespace[k] = make_getter(namespace[k])
        return super().__new__(mcs, name, bases, namespace)


class FormatDict(dict):
    """Dict to replace missing keys."""

    def __missing__(self, key: str) -> str:
        """Replace missing key with '{key}'."""
        return '{' + key + '}'


class Component(metaclass=_Maker):  # pylint: disable=too-few-public-methods
    """Abstract class for all components.

    All visual and control classes subclass this so their events
    and commands get transformed by the metaclass.
    """

    _NEXT_UUID = 0  # type: ClassVar[int]

    @property
    @abstractmethod
    def _TEMPLATE(self): pass  # pylint: disable=invalid-name,multiple-statements

    @property
    @abstractmethod
    def _COMPONENT(self): pass  # pylint: disable=invalid-name,multiple-statements

    @property
    @abstractmethod
    def _PACKAGE(self): pass  # pylint: disable=invalid-name,multiple-statements

    @property
    @abstractmethod
    def _ATTRS(self): pass  # pylint: disable=invalid-name,multiple-statements

    @property
    @abstractmethod
    def _instantiate(self): pass  # pylint: disable=invalid-name,multiple-statements

    @classmethod
    def _next_uuid(cls) -> int:
        cls._NEXT_UUID += 1
        return cls._NEXT_UUID

    def __init__(self) -> None:
        """Give the component a unique ID."""
        # wanted to put "self" instead of "Component"
        # was surprised that didn't work
        self._uuid = Component._next_uuid()
        super().__init__()
        self._tagbase = " socket={{socket}} uuid={{'{uuid}'}} />".format(uuid=self._uuid)
        self._tag = '<' + self._COMPONENT
        if self._ATTRS:
            self._tag += ' ' + self._ATTRS
        self._comp = None
        COMPONENT_REGISTRY[self._uuid] = self

    @staticmethod
    def _insert(wrap: str, tag: Optional[str]) -> str:
        """Insert the component tag into the wrapper html.

        This ignores other tags already created like ``{socket}``.

        https://stackoverflow.com/a/11284026/744520
        """
        if tag is None:
            raise ValueError('tag cannot be None')
        formatter = string.Formatter()
        mapping = FormatDict(component=tag)
        return formatter.vformat(wrap, (), mapping)
