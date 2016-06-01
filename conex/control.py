# -*- coding: utf-8 -*-

from collections import namedtuple

import numpy as np
from enum import Enum

from conex.component import Component

# from event import Event


class Controller(Component):
    """
    Used to test if a an object is a controller.
    All controllers must inherit this class.
    """
    pass


class Nouislider(Controller):
    template = 'nouislider.jsx'
    package = 'react-nouislider'
    tag = ('<Nouislider range={{{{min: {min}, max: {max}}}}} '
           'start={{{start}}} {tooltips} '
           'onChange={{ function(x) {{socket.emit("{uuid}#change", x);}} }} '
           '/>')



    def __init__(self, start=0, minimum=0, maximum=100, tooltips=False):
        super(Nouislider, self).__init__()
        start = np.atleast_1d(start)
        self.instantiate = self.tag.format(
            uuid=self._uuid,
            min=minimum,
            max=maximum,
            start=start,
            tooltips='tooltips' if tooltips else ''
        )

    def on_update(self):
        pass

    def on_slide(self):
        pass

    def on_set(self):
        pass

    def on_change(self):
        pass

    def on_start(self):
        pass

    def on_en(self):
        pass
