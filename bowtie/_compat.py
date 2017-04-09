# -*- coding: utf-8 -*-
"""Python 2/3 compatability."""

import inspect
import sys
from os import makedirs

IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    # pylint: disable=invalid-name
    makedirs_lib = makedirs
    # pylint: disable=function-redefined,missing-docstring
    def makedirs(name, mode=0o777, exist_ok=False):
        """Create directories recursively."""
        try:
            makedirs_lib(name, mode=mode)
        except OSError:
            if not exist_ok:
                raise

def numargs(func):
    """Get number of arguments in Python 3."""
    return len(inspect.signature(func).parameters)

if IS_PY2:
    # pylint: disable=function-redefined
    def numargs(func):
        """Get number of arguments in Python 2."""
        count = 0
        # pylint: disable=deprecated-method
        for args in inspect.getargspec(func)[:2]:
            try:
                count += len(args)
            except TypeError:
                pass
        return count
