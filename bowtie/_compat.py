# -*- coding: utf-8 -*-
"""
python 2/3 compatability
"""

import inspect
import sys
from os import makedirs

IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    # pylint: disable=invalid-name
    makedirs_lib = makedirs
    # pylint: disable=function-redefined,missing-docstring
    def makedirs(name, mode=0o777, exist_ok=False):
        try:
            makedirs_lib(name, mode=mode)
        except OSError:
            if not exist_ok:
                raise

def numargs(func):
    return len(inspect.signature(func).parameters)

if IS_PY2:
    # pylint: disable=function-redefined,missing-docstring
    def numargs(func):
        return sum(map(len, inspect.getargspec(func)[:2]))

# def var_name(x):
#     gen = globals().items()
#     # print(globals())
#     for k, v in gen:
#         print(k)
#         if x is v:
#             return k


# def varname(var):
#     import inspect
#     frame = inspect.stack()[0][0].f_globals
#     var_id = id(var)
#     for name in frame.f_back.f_locals.keys():
#         try:
#             if id(eval(name)) == var_id:
#                 return(name)
#         except:
#             pass
