# -*- coding: utf-8 -*-
"""Visual components."""

from flask import Markup
from markdown import markdown

from bowtie._component import Component, jdumps, jsbool
from bowtie._progress import Progress


# pylint: disable=too-few-public-methods
class _Visual(Component):
    """Abstract class all visual components inherit.

    Used to test if a an object is a visual component.
    """

    def __init__(self):
        self.progress = Progress()
        super(_Visual, self).__init__()

    @property
    def _instantiate(self):
        # pylint: disable=protected-access
        begin, end = self.progress._tags
        tagwrap = begin + '{component}' + self._tagbase + end
        return self._insert(tagwrap, self._comp)


class Markdown(_Visual):
    """Display Markdown."""

    _TEMPLATE = 'markdown.jsx'
    _COMPONENT = 'Markdown'
    _PACKAGE = None
    _ATTRS = "initial={{'{initial}'}}"

    def __init__(self, initial=''):
        """Create a Markdown widget.

        Parameters
        ----------
        initial : str, optional
            Default markdown for the widget.

        """
        super(Markdown, self).__init__()

        self._comp = self._tag.format(
            initial=Markup(markdown(initial).replace('\n', '\\n'))
        )

    # pylint: disable=no-self-use
    def do_text(self, text):
        """Replace widget with this text.

        Parameters
        ----------
        test : str
            Markdown text as a string.

        Returns
        -------
        None

        """
        return Markup(markdown(text))

    def get(self, text):
        """Get the current text.

        Returns
        -------
        String of html.

        """
        return text


class Table(_Visual):
    """Ant Design table with filtering and sorting."""

    _TEMPLATE = 'table.jsx'
    _COMPONENT = 'AntTable'
    _PACKAGE = None
    _ATTRS = ('columns={{{columns}}} '
              'resultsPerPage={{{results_per_page}}}')

    def __init__(self, data=None, columns=None, results_per_page=10):
        """Create a table and optionally intialize the data.

        Parameters
        ----------
        columns : list, optional
            List of column names to display.
        results_per_page : int, optional
            Number of rows on each pagination of the table.

        """
        super(Table, self).__init__()
        self.data = []
        self.columns = []
        if data:
            self.data, self.columns = self._make_data(data)
        elif columns:
            self.columns = self._make_columns(columns)

        self.results_per_page = results_per_page

        self._comp = self._tag.format(
            columns=self.columns,
            results_per_page=self.results_per_page
        )

    @staticmethod
    def _make_columns(columns):
        """Transform list of columns into AntTable format."""
        return [dict(title=str(c),
                     dataIndex=str(c),
                     key=str(c))
                for c in columns]

    @staticmethod
    def _make_data(data):
        """Transform table data into JSON."""
        jsdata = []
        for idx, row in data.iterrows():
            row.index = row.index.astype(str)
            rdict = row.to_dict()
            rdict.update(dict(key=str(idx)))
            jsdata.append(rdict)

        return jsdata, Table._make_columns(data.columns)

    # pylint: disable=no-self-use
    def do_data(self, data):
        """Replace the columns and data of the table.

        Parameters
        ----------
        data : pandas.DataFrame

        Returns
        -------
        None

        """
        return self._make_data(data)

    def do_columns(self, columns):
        """Update the columns of the table.

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
    """Griddle table with filtering and sorting."""

    _TEMPLATE = 'griddle.jsx'
    _COMPONENT = 'SmartGrid'
    _PACKAGE = 'griddle-react@version0'
    _ATTRS = ('columns={{{columns}}} '
              'resultsPerPage={{{results_per_page}}}')

    def __init__(self, columns=None, results_per_page=10):
        """Create the table, optionally set the columns.

        Parameters
        ----------
        columns : list, optional
            List of column names to display.
        results_per_page : int, optional
            Number of rows on each pagination of the table.

        """
        super(SmartGrid, self).__init__()
        if columns is None:
            columns = []
        self.columns = columns
        self.results_per_page = results_per_page

        self._comp = self._tag.format(
            columns=jdumps(self.columns),
            results_per_page=self.results_per_page
        )

    # pylint: disable=no-self-use
    def do_update(self, data):
        """Update the data of the table.

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
        Get the table data.

        Returns
        -------
        list
            Each entry in the list is a dict of labels and values for a row.

        """
        return data


class SVG(_Visual):
    """SVG image.

    Mainly for matplotlib plots.
    """

    _TEMPLATE = 'svg.jsx'
    _COMPONENT = 'SVG'
    _PACKAGE = None
    _ATTRS = 'preserve_aspect_ratio={{{preserve_aspect_ratio}}}'

    def __init__(self, preserve_aspect_ratio=False):
        """Create SVG component.

        Parameters
        ----------
        preserve_aspect_ratio : bool, optional
            If ``True`` it preserves the aspect ratio otherwise
            it will stretch to fill up the space available.

        """
        super(SVG, self).__init__()
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self._comp = self._tag.format(
            preserve_aspect_ratio=jsbool(self.preserve_aspect_ratio)
        )

    # pylint: disable=no-self-use
    def do_image(self, image):
        """Replace the image.

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
    """Plotly component.

    Useful for many kinds of plots.
    """

    _TEMPLATE = 'plotly.jsx'
    _COMPONENT = 'PlotlyPlot'
    _PACKAGE = 'plotly.js'
    _ATTRS = 'initState={{{init}}}'

    def __init__(self, init=None):
        """Create a Plotly component.

        Parameters
        ----------
        init : dict, optional
            Initial Plotly data to plot.

        """
        super(Plotly, self).__init__()
        if init is None:
            init = dict(data=[], layout={'autosize': False})
        self.init = init

        self._comp = self._tag.format(
            init=jdumps(self.init)
        )

    ## Events

    def on_click(self):
        """React to Plotly click event.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_click

    def on_beforehover(self):
        """Emit an event before hovering over a point.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_hover

    def on_hover(self):
        """Emit an event after hovering over a point.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_hover

    def on_unhover(self):
        """Emit an event when hover is removed.

        | **Payload:** TODO.

        Returns
        -------
        str
            Name of event.

        """
        return self.get_hover

    def on_select(self):
        """Emit an event when points are selected with a tool.

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
        """Replace the entire plot.

        Parameters
        ----------
        plot : dict
            Dict that can be plotted with Plotly.
            It should have this structure: ``{data: [], layout: {}}``.

        Returns
        -------
        None

        """
        return plot

    def do_data(self, data):
        """Replace the data portion of the plot.

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
        """Update the layout.

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
        """Update the configuration of the plot.

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
        """Get the current selection of points.

        Returns
        -------
        list

        """
        return data

    def get_select(self, data):
        """Get the current selection of points.

        Returns
        -------
        list

        """
        return data

    def get_click(self, data):
        """Get the current selection of points.

        Returns
        -------
        list

        """
        return data

    def get_hover(self, data):
        """Get the current selection of points.

        Returns
        -------
        list

        """
        return data
