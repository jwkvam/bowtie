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
    It can be accessed through the ``.progress`` accessor.

    Examples
    --------
    >>> plotly = Plotly()
    >>> def callback(x):
    >>>     plotly.progress.do_visible(True)
    >>>     plotly.progress.do_percent(0)
    >>>     compute1()
    >>>     plotly.progress.do_inc(50)
    >>>     compute2()
    >>>     plotly.progress.do_visible(False)

    """
    _TEMPLATE = 'progress.jsx'
    _COMPONENT = 'CProgress'
    _PACKAGE = 'antd'
    _TAG = ('<CProgress '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '>')

    def _instantiate(self):
        return self._TAG.format(
            uuid="'{}'".format(self._uuid)
        )

    # pylint: disable=no-self-use
    def do_percent(self, percent):
        """Set the percentage of the progress.

        Parameters
        ----------
        percent : number
            Sets the progress to this percentage.

        Returns
        -------
        None

        """
        return percent

    def do_inc(self, inc):
        """Increments the progress indicator.

        Parameters
        ----------
        inc : number
            Value to increment the progress.

        Returns
        -------
        None

        """
        return inc

    def do_visible(self, visible):
        """Hides and shows the progress indicator.

        Parameters
        ----------
        visible : bool
            If ``True`` shows the progress indicator
            otherwise it is hidden.

        Returns
        -------
        None

        """
        return visible

    def do_active(self):
        """Hides and shows the progress indicator.

        Returns
        -------
        None

        """
        pass

    def do_success(self):
        """Hides and shows the progress indicator.

        Returns
        -------
        None

        """
        pass

    def do_error(self):
        """Hides and shows the progress indicator.

        Returns
        -------
        None

        """
        pass
