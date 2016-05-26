# -*- coding: utf-8 -*-


from enum import Enum
###
# p1 = Plotly('helo')
# p2 = Plotly('helo')
# p2.subscribe(p1.events.click, lambda x: x)

import string

from conex.component import Component


class Visual(Component):
    """
    Used to test if a an object is a controller.
    All controllers must inherit this class.
    """
    pass


class Plotly(Visual):
    template = 'plotly.jsx'
    package = 'plotly.js'
    tag = '<PlotlyPlot />'

    _events = ['click']

    def __init__(self, data=None, layout=None):
        self.instantiate = self.tag
        super(Plotly, self).__init__()

    # events = Enum('Events', ['click',
    #                          'before_hover',
    #                          'hover',
    #                          'unhover',
    #                          'select'])




