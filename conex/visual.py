# -*- coding: utf-8 -*-


from collections import namedtuple
import json

from future.utils import with_metaclass

from flask_socketio import emit
from conex.component import Component, _EventMeta


def make_command(command):

    def actualcommand(self, data):
        name = command.__name__[3:]
        signal = '{uuid}#{event}'.format(uuid=self._uuid, event=name)
        print(signal)
        return emit(signal, json.dumps(data))

    actualcommand.__doc__ = command.__doc__

    return actualcommand


def is_command(attribute):
    return attribute.startswith('do_')


class _CommandMeta(_EventMeta):
    def __new__(cls, name, parents, dct):
        for k in dct:
            if is_command(k):
                dct[k] = make_command(dct[k])
        return super(_CommandMeta, cls).__new__(cls, name, parents, dct)


class Visual(with_metaclass(_CommandMeta, Component)):
    """
    Used to test if a an object is a controller.
    All controllers must inherit this class.
    """
    def __init__(self):
        super(Visual, self).__init__()


class Table(Visual):
    template = 'datagrid.jsx'
    component = 'Table'
    package = 'react-datagrid'
    tag = ('<Table '
           'socket={{socket}} '
           'uuid={{{uuid}}} '
           '/>')

    def __init__(self):
        super(Table, self).__init__()

    def instantiate(self, columns, rows):
        return self.tag.format(
            uuid="'{}'".format(self._uuid),
        )


    ## Events

    # def on_click(self):
    #     pass
    #
    # def on_beforehover(self):
    #     pass
    #
    # def on_hover(self):
    #     pass
    #
    # def on_unhover(self):
    #     pass
    #
    # def on_selected(self):
    #     pass
    #
    # ## Commands
    #
    # def do_all(self, data):
    #     pass
    #
    # def do_data(self, data):
    #     pass
    #
    # def do_layout(self, data):
    #     pass
    #
    # def do_config(self, data):
    #     pass

class Plotly(Visual):
    template = 'plotly.jsx'
    component = 'PlotlyPlot'
    package = 'plotly.js'
    tag = ('<PlotlyPlot initState={{{init}}} '
           'socket={{socket}} '
           'uuid={{{uuid}}} '
           'rows={{{rows}}} '
           'columns={{{columns}}} '
           '/>')

    def __init__(self, init=None):
        super(Plotly, self).__init__()
        if init is None:
            init = dict(data=[], layout={'autosize': True})
        self.init = init

    def instantiate(self, columns, rows):
        return self.tag.format(
            uuid="'{}'".format(self._uuid),
            init=json.dumps(self.init),
            rows=rows,
            columns=columns
        )


    ## Events

    def on_click(self):
        pass

    def on_beforehover(self):
        pass

    def on_hover(self):
        pass

    def on_unhover(self):
        pass

    def on_selected(self):
        pass

    ## Commands

    def do_all(self, data):
        pass

    def do_data(self, data):
        pass

    def do_layout(self, data):
        pass

    def do_config(self, data):
        pass
