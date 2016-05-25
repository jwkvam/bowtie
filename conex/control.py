# -*- coding: utf-8 -*-

from enum import Enum

import numpy as np

from conex.component import Component


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
           'start={{{start}}} {tooltips} />')

    def __init__(self, start=0, minimum=0, maximum=100, tooltips=False):
        start = np.atleast_1d(start)
        self.instantiate = self.tag.format(
            min=minimum,
            max=maximum,
            start=start,
            tooltips='tooltips' if tooltips else ''
        )
        super(Nouislider, self).__init__()

    # pass
    #events = Enum('Events', [''])kkk
