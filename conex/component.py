# -*- coding: utf-8 -*-

from flask_socketio import emit
from future.utils import with_metaclass
from eventlet.event import Event


def make_event(event):

    @property
    def actualevent(self):
        name = event.__name__[3:]
        return '{uuid}#{event}'.format(uuid=self._uuid, event=name)

    # TODO fix this for python 2
    # actualevent.__doc__ = event.__doc__

    return actualevent


def is_event(attribute):
    return attribute.startswith('on_')


class _EventMeta(type):
    def __new__(cls, name, parents, dct):
        for k in dct:
            if is_event(k):
                dct[k] = make_event(dct[k])
        return super(_EventMeta, cls).__new__(cls, name, parents, dct)


class Component(with_metaclass(_EventMeta, object)):
    _NEXT_UUID = 0

    @classmethod
    def _next_uuid(cls):
        cls._NEXT_UUID += 1
        return cls._NEXT_UUID

    def __init__(self):
        # TODO wanted to put "self" instead of "Component"
        # was surprised that didn't work
        self._uuid = Component._next_uuid()
        super(Component, self).__init__()

    def get(self, block=True, timeout=None):
        event = Event()
        emit('{}#get'.format(self._uuid), callback=lambda x: event.send(x))
        return event.wait()
