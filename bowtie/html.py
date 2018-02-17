# -*- coding: utf-8 -*-
"""Static HTML Components."""


# pylint: disable=too-few-public-methods
class Div:
    """Div tag."""

    pass


class Header:
    """Header tag."""

    def __init__(self, text: str, size: int = 1) -> None:
        """Create header text with a size.

        Parameters
        ----------
        text : str
            Text of the header tag.
        size : int
            Size of the header tag from 1 to 6.

        """
        if size not in range(1, 7):
            raise ValueError('Header size must be in [1..6], found {}.'.format(size))
        self.size = size
        self.text = text
