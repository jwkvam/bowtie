# -*- coding: utf-8 -*-

from collections import namedtuple

from inspect import stack

from flask.ext.socketio import emit

from uuid import uuid4

from future.utils import with_metaclass

from eventlet.queue import LightQueue
from eventlet.event import Event


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
        self.queue = LightQueue()

    def _get_queue(self):
        for i, f in enumerate(stack(0)):
            # if 'flask_socketio' in f[1] and '_handle' in f[3]:
            if 'flask/ctx.py' in f[1] and 'wrapper' in f[3]:
                break
        name = self.__class__.__name__
        # import IPython
        # IPython.embed()
        return stack(0)[i-1][0].f_globals['queue_{}_{}'.format(name, self._uuid)]



    def get(self, block=True, timeout=None):
        # queue = self._get_queue()
        # def getting():
        #     valx = queue.get(block=block, timeout=10)
        #     print('spwaned', valx)
        #     return valx
        event = Event()
        def ack(data):
            print('acknowledged')
            print(data)
            # valx = queue.put(data)
            event.send(data)
        emit('{}#get'.format(self._uuid), callback=ack)
        print('wait get')
        val = [1]
        # valx = queue.get(block=block, timeout=10)
        valx = event.wait()
        # eventlet.spawn(getting)
        #
        # eventlet.sleep(1)
        # print(valx)
        print('done get', valx)
        return val
