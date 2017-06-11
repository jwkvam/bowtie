# -*- coding: utf-8 -*-
"""Progress component.

Not for direct use by user.
"""

from bowtie._component import Component


class Progress(Component):
    """Circle progress indicator."""

    _TEMPLATE = 'progress.jsx'
    _COMPONENT = 'AntProgress'
    _PACKAGE = None
    _ATTRS = None

    def __init__(self):
        """Create a progress indicator.

        This component is used by all visual components.
        It is not meant to be used alone.

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

        References
        ----------
        https://ant.design/components/progress/

        """
        super(Progress, self).__init__()
        self._tagbase = self._tagbase[:-3] + '>'
        self._tags = '<' + self._COMPONENT + self._tagbase, '</AntProgress>'

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
        """Increment the progress indicator.

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
        """Hide and shows the progress indicator.

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
        """Reset the progress to active (in progress) status.

        Returns
        -------
        None

        """
        pass

    def do_success(self):
        """Display the progress indicator as done.

        Returns
        -------
        None

        """
        pass

    def do_error(self):
        """Display an error in the progress indicator.

        Returns
        -------
        None

        """
        pass
