# -*- coding: utf-8 -*-

from collections import namedtuple

from uuid import uuid4

class Component(object):

    def __init__(self):
        self.uuid = id(self)

        self._Events = namedtuple('_Events', self._events)
        self.events = self._Events(**{e: '{}#{}'.format(self.uuid, e)
                                      for e in self._events})
