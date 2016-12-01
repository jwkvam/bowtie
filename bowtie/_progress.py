# -*- coding: utf-8 -*-
"""
Progress component
"""

from bowtie._component import Component


class Progress(Component):
    """This component is used by all visual components and
    is not meant to be used alone.

    By default, it is not visible.
    It is an opt-in feature and you can happily use Bowtie
    without using the progress indicators at all.

    It is useful for indicating progress to the user for long-running processes.
    It can be accessed through the `.progress` accessor.

    For example:

    >>> plotly = Plotly()
    >>> def callback(x):
    >>>     plotly.do_visible(True)
    >>>     plotly.do_inc(3)
    >>>     plotly.do_visible(False)

    """
    _TEMPLATE = 'progress.jsx'
    _COMPONENT = 'Progress'
    _PACKAGE = 'rc-progress'
    _TAG = ('<Progress '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            'color={{{color}}} '
            '>')

    def __init__(self, color='#91a8d0'):
        self.color = color
        super(Progress, self).__init__()

    def _instantiate(self):
        return self._TAG.format(
            uuid="'{}'".format(self._uuid),
            color="'{}'".format(self.color)
        )

    def do_percent(self, data):
        pass

    def do_inc(self, data):
        pass

    def do_visible(self, data):
        pass
