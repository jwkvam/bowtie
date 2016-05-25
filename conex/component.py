# -*- coding: utf-8 -*-

from uuid import uuid4

class Component(object):

    def __init__(self):
        self.uuid = str(uuid4())
