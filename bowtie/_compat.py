# -*- coding: utf-8 -*-
"""
python 2/3 compatability
"""

import sys
from os import makedirs

if sys.version_info < (3, 0):
    # pylint: disable=invalid-name
    makedirs_lib = makedirs
    # pylint: disable=function-redefined,missing-docstring
    def makedirs(name, mode=0o777, exist_ok=False):
        try:
            makedirs_lib(name, mode=mode)
        except OSError:
            if not exist_ok:
                raise
