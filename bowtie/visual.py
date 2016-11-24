# -*- coding: utf-8 -*-
"""
Visual components
"""

from bowtie._component import Component, jdumps


class _Progress(Component):
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
        super(_Progress, self).__init__()

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


# pylint: disable=too-few-public-methods
class _Visual(Component):
    """
    Used to test if a an object is a controller.
    All controllers must inherit this class.
    """
    def __init__(self, progress_color):
        progress_args = {}
        if progress_color:
            progress_args['color'] = progress_color
        self.progress = _Progress(**progress_args)
        super(_Visual, self).__init__()


class SmartGrid(_Visual):
    """Table Component with filtering and sorting

    Parameters
    ----------
    columns : list, optional
        List of column names to display.
    results_per_page : int, optional
        Number of rows on each pagination of the table.

    """
    _TEMPLATE = 'griddle.jsx'
    _COMPONENT = 'SmartGrid'
    _PACKAGE = 'griddle-react'
    _TAG = ('<SmartGrid '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            'columns={{{columns}}} '
            'resultsPerPage={{{results_per_page}}}'
            '/>')

    def __init__(self, columns=None, results_per_page=10,
                 progress_color=None):
        if columns is None:
            columns = []
        self.columns = columns
        self.results_per_page = results_per_page
        super(SmartGrid, self).__init__(progress_color=progress_color)

    def _instantiate(self):
        return self._TAG.format(
            uuid="'{}'".format(self._uuid),
            columns=jdumps(self.columns),
            results_per_page=self.results_per_page
        )

    def do_update(self, data):
        pass

#
# TODO: these visuals are partially implemented
# class FixedTable(_Visual):
#     _TEMPLATE = 'fixedtable.jsx'
#     _COMPONENT = 'FixedTable'
#     _PACKAGE = 'fixed-data-table'
#     _TAG = ('<FixedTable '
#            'socket={{socket}} '
#            'uuid={{{uuid}}} '
#            'rows={{{rows}}} '
#            'columns={{{columns}}} '
#            '/>')
#
#     def __init__(self):
#         super(FixedTable, self).__init__()
#
#     def _instantiate(self, columns, rows):
#         return self._TAG.format(
#             uuid="'{}'".format(self._uuid),
#             rows=rows,
#             columns=columns
#         )
#
#
# class DataTable(_Visual):
#     _TEMPLATE = 'datatables.jsx'
#     _COMPONENT = 'JTable'
#     _PACKAGE = 'react-jquery-datatables'
#     _TAG = ('<JTable '
#            'socket={{socket}} '
#            'uuid={{{uuid}}} '
#            '/>')
#
#     def __init__(self):
#         super(DataTable, self).__init__()
#
#     def _instantiate(self, columns, rows):
#         return self._TAG.format(
#             uuid="'{}'".format(self._uuid),
#         )
#
#
# class Grid(_Visual):
#     _TEMPLATE = 'dazzlegrid.jsx'
#     _COMPONENT = 'Grid'
#     _PACKAGE = 'react-data-grid'
#     _TAG = ('<Grid '
#            'socket={{socket}} '
#            'uuid={{{uuid}}} '
#            '/>')
#
#     def __init__(self):
#         super(Grid, self).__init__()
#
#     def _instantiate(self, columns, rows):
#         return self._TAG.format(
#             uuid="'{}'".format(self._uuid),
#         )
#
#
# class Table(_Visual):
#     _TEMPLATE = 'datagrid.jsx'
#     _COMPONENT = 'Table'
#     _PACKAGE = 'react-datagrid'
#     _TAG = ('<Table '
#            'socket={{socket}} '
#            'uuid={{{uuid}}} '
#            '/>')
#
#     def __init__(self):
#         super(Table, self).__init__()
#
#     def _instantiate(self, columns, rows):
#         return self._TAG.format(
#             uuid="'{}'".format(self._uuid),
#         )


class Plotly(_Visual):
    """
    Plotly component.
    """
    _TEMPLATE = 'plotly.jsx'
    _COMPONENT = 'PlotlyPlot'
    _PACKAGE = 'plotly.js'
    _TAG = ('<PlotlyPlot initState={{{init}}} '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, init=None, progress_color=None):
        if init is None:
            init = dict(data=[], layout={'autosize': False})
        self.init = init
        super(Plotly, self).__init__(progress_color=progress_color)

    def _instantiate(self):
        return self._TAG.format(
            uuid="'{}'".format(self._uuid),
            init=jdumps(self.init),
        )


    ## Events

    def on_click(self):
        """Plotly click event.

        Returns
        -------
        str
            Name of click event.

        """
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
