# -*- coding: utf-8 -*-

from collections import namedtuple
from datetime import datetime
import json

from future.utils import with_metaclass

from flask_socketio import emit
from bowtie.component import Component


def json_conversion(obj):

    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError('Not sure how to serialize {} of type {}'.format(obj, type(obj)))


def jdumps(data):
    return json.dumps(data, default=json_conversion)


 #with_metaclass(_CommandMeta, Component)):
class Visual(Component):
    """
    Used to test if a an object is a controller.
    All controllers must inherit this class.
    """
    pass
    # def __init__(self):
    #     super(Visual, self).__init__()


class SmartGrid(Visual):
    template = 'griddle.jsx'
    component = 'SmartGrid'
    package = 'griddle-react'
    tag = ('<SmartGrid '
           'socket={{socket}} '
           'uuid={{{uuid}}} '
           'rows={{{rows}}} '
           'columns={{{columns}}} '
           '/>')

    def __init__(self):
        super(SmartGrid, self).__init__()

    def instantiate(self, columns, rows):
        return self.tag.format(
            uuid="'{}'".format(self._uuid),
            rows=rows,
            columns=columns
        )

    def do_update(self, data):
        pass

class FixedTable(Visual):
    template = 'fixedtable.jsx'
    component = 'FixedTable'
    package = 'fixed-data-table'
    tag = ('<FixedTable '
           'socket={{socket}} '
           'uuid={{{uuid}}} '
           'rows={{{rows}}} '
           'columns={{{columns}}} '
           '/>')

    def __init__(self):
        super(FixedTable, self).__init__()

    def instantiate(self, columns, rows):
        return self.tag.format(
            uuid="'{}'".format(self._uuid),
            rows=rows,
            columns=columns
        )


class DataTable(Visual):
    template = 'datatables.jsx'
    component = 'JTable'
    package = 'react-jquery-datatables'
    tag = ('<JTable '
           'socket={{socket}} '
           'uuid={{{uuid}}} '
           '/>')

    def __init__(self):
        super(DataTable, self).__init__()

    def instantiate(self, columns, rows):
        return self.tag.format(
            uuid="'{}'".format(self._uuid),
        )


class Grid(Visual):
    template = 'dazzlegrid.jsx'
    component = 'Grid'
    package = 'react-data-grid'
    tag = ('<Grid '
           'socket={{socket}} '
           'uuid={{{uuid}}} '
           '/>')

    def __init__(self):
        super(Grid, self).__init__()

    def instantiate(self, columns, rows):
        return self.tag.format(
            uuid="'{}'".format(self._uuid),
        )


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
            init=jdumps(self.init),
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

    def on_select(self):
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
