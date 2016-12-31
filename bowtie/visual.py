# -*- coding: utf-8 -*-
"""
Visual components
"""

from bowtie._component import Component, jdumps
from bowtie._progress import Progress


# pylint: disable=too-few-public-methods
class _Visual(Component):
    """
    Used to test if a an object is a controller.
    All controllers must inherit this class.
    """
    def __init__(self):
        self.progress = Progress()
        super(_Visual, self).__init__()


class Table(_Visual):
    """Table Component with filtering and sorting

    Parameters
    ----------
    columns : list, optional
        List of column names to display.
    results_per_page : int, optional
        Number of rows on each pagination of the table.

    """
    _TEMPLATE = 'table.jsx'
    _COMPONENT = 'AntTable'
    _PACKAGE = 'antd'
    _TAG = ('<AntTable '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            'columns={{{columns}}} '
            'resultsPerPage={{{results_per_page}}} '
            '/>')

    def __init__(self, data=None, columns=None, results_per_page=10):
        self.data = []
        self.columns = []
        if data:
            self.data, self.columns = self._make_data(data)
        elif columns:
            self.columns = self._make_columns(columns)

        self.results_per_page = results_per_page
        super(Table, self).__init__()

    def _instantiate(self):
        return self._TAG.format(
            uuid="'{}'".format(self._uuid),
            columns=self.columns,
            results_per_page=self.results_per_page
        )

    @staticmethod
    def _make_columns(columns):
        """
        doc
        """
        return [dict(title=str(c),
                     dataIndex=str(c),
                     key=str(c))
                for c in columns]

    @staticmethod
    def _make_data(data):
        """
        doc
        """
        jsdata = []
        for idx, row in data.iterrows():
            row.index = row.index.astype(str)
            rdict = row.to_dict()
            rdict.update(dict(key=str(idx)))
            jsdata.append(rdict)

        return jsdata, Table._make_columns(data.columns)

    # pylint: disable=no-self-use
    def do_data(self, data):
        """Replaces the columns and data of the table.

        Parameters
        ----------
        data : pandas.DataFrame

        Returns
        -------
        None

        """
        return self._make_data(data)

    def do_columns(self, columns):
        """Updates the columns of the table

        Parameters
        ----------
        columns : array-like
            List of strings.

        Returns
        -------
        None

        """
        return self._make_columns(columns)


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

    def __init__(self, columns=None, results_per_page=10):
        if columns is None:
            columns = []
        self.columns = columns
        self.results_per_page = results_per_page
        super(SmartGrid, self).__init__()

    def _instantiate(self):
        return self._TAG.format(
            uuid="'{}'".format(self._uuid),
            columns=jdumps(self.columns),
            results_per_page=self.results_per_page
        )

    # pylint: disable=no-self-use
    def do_update(self, data):
        """Updates the data of the table

        Parameters
        ----------
        data : list of dicts
            Each entry in the list must be a dict
            with the same keys which are the columns
            of the table.

        Returns
        -------
        None

        """
        return data

    def get(self, data):
        """
        Gets the table data.

        Returns
        -------
        list
            Each entry in the list is a dict of labels and values for a row.
        """
        return data


class SVG(_Visual):
    """SVG image, mainly for matplotlib plots.

    Parameters
    ----------
    preserve_aspect_ratio : bool, optional
        If ``True`` it preserves the aspect ratio otherwise
        it will stretch to fill up the space available.

    """
    _TEMPLATE = 'svg.jsx'
    _COMPONENT = 'SVG'
    _PACKAGE = None
    _TAG = ('<SVG '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            'preserve_aspect_ratio={{{preserve_aspect_ratio}}} '
            '/>')

    def __init__(self, preserve_aspect_ratio=False):
        self.preserve_aspect_ratio = preserve_aspect_ratio
        super(SVG, self).__init__()

    def _instantiate(self):
        return self._TAG.format(
            uuid="'{}'".format(self._uuid),
            preserve_aspect_ratio='true' if self.preserve_aspect_ratio else 'false'
        )

    # pylint: disable=no-self-use
    def do_image(self, image):
        """Replaces the image.

        Parameters
        ----------
        image : str
            Generated by ``savefig`` from matplotlib with ``format=svg``.

        Returns
        -------
        None

        Examples
        --------
        >>> from io import StringIO
        >>> import matplotlib
        >>> matplotlib.use('Agg')
        >>> import matplotlib.pyplot as plt
        >>> image = SVG()
        >>>
        >>> def callback(x):
        >>>     sio = StringIO()
        >>>     plt.plot(range(5))
        >>>     plt.savefig(sio, format='svg')
        >>>     sio.seek(0)
        >>>     s = sio.read()
        >>>     idx = s.find('<svg')
        >>>     s = s[idx:]
        >>>     image.do_image(s)

        """
        return image


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

    def __init__(self, init=None):
        if init is None:
            init = dict(data=[], layout={'autosize': False})
        self.init = init
        super(Plotly, self).__init__()

    def _instantiate(self):
        return self._TAG.format(
            uuid="'{}'".format(self._uuid),
            init=jdumps(self.init),
        )

    ## Events

    def on_click(self):
        """Plotly click event.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_click

    def on_beforehover(self):
        """Emits an event before hovering over a point.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_hover

    def on_hover(self):
        """Emits an event after hovering over a point.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_hover

    def on_unhover(self):
        """Emits an event when hover is removed.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_hover

    def on_select(self):
        """Emits an event when points are selected with a tool.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_select

    ## Commands

    # pylint: disable=no-self-use
    def do_all(self, plot):
        """Replaces the entire plot.

        Parameters
        ----------
        plot : dict
            Dict that can be plotted with Plotly.

        Returns
        -------
        None

        """
        return plot

    def do_data(self, data):
        """Replaces the data portion of the plot.

        Parameters
        ----------
        data : list of traces
            List of data to replace the old data.

        Returns
        -------
        None

        """
        return data

    def do_layout(self, layout):
        """Updates the layout.

        Parameters
        ----------
        layout : dict
            Contains layout information.

        Returns
        -------
        None

        """
        return layout

    def do_config(self, config):
        """Updates the configuration of the plot.

        Parameters
        ----------
        config : dict
            Plotly config information.

        Returns
        -------
        None

        """
        return config

    def get(self, data):
        """
        Gets the current selection of points.

        Returns
        -------
        list
        """
        return data

    def get_select(self, data):
        """
        Gets the current selection of points.

        Returns
        -------
        list
        """
        return data

    def get_click(self, data):
        """
        Gets the current selection of points.

        Returns
        -------
        list
        """
        return data

    def get_hover(self, data):
        """
        Gets the current selection of points.

        Returns
        -------
        list
        """
        return data
