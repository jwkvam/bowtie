# -*- coding: utf-8 -*-

import sys
from os import makedirs

from builtins import bytes

import dill as pickle

if sys.version_info < (3, 0):
    makedirs_lib = makedirs
    def makedirs(name, mode=0o777, exist_ok=False):
        try:
            makedirs_lib(name, mode=mode)
        except OSError:
            if not exist_ok:
                raise

def dumps(x):
    dump = pickle.dumps(x)
    if sys.version_info < (3, 0):
        dump = bytes(dump.encode('string-escape'))
    return dump
