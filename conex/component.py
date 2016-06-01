# -*- coding: utf-8 -*-

from collections import namedtuple

from uuid import uuid4


from future.utils import with_metaclass


def make_event(event):

    @property
    def actualevent(self):
        name = event.__name__[3:]
        return '{uuid}#{event}'.format(uuid=self._uuid, event=name)

    actualevent.__doc__ = event.__doc__

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

    def __init__(self):
        self._uuid = id(self)
