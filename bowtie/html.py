# -*- coding: utf-8 -*-
"""Static HTML Components."""


class Div:
    pass


class Header:

    def __init__(self, level):
        pass


class Link:
    """An internal link.

    This doesn't create a page reload.
    """

    _TEMPLATE = 'link.jsx'
    _COMPONENT = 'ALink'
    _PACKAGE = None
    _ATTRS = "to={{'{link}'}}"

    def __init__(self) -> None:
        """Create a button.

        Parameters
        ----------
        link : str

        """
        pass
