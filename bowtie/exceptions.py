# -*- coding: utf-8 -*-
"""Custom Bowtie exceptions."""


class YarnError(Exception):
    """Errors from ``Yarn``."""

    pass


class WebpackError(Exception):
    """Errors from ``Webpack``."""

    pass


class SizeError(Exception):
    """Size values must be a number."""

    pass


class GridIndexError(IndexError):
    """Invalid index into the grid layout."""

    pass


class NoUnusedCellsError(Exception):
    """All cells are used."""

    pass


class UsedCellsError(Exception):
    """All cells are used."""

    pass


class MissingRowOrColumn(Exception):
    """Missing a row or column."""

    pass


class NoSidebarError(Exception):
    """Cannot add to the sidebar when it doesn't exist."""

    pass


class NotStatefulEvent(Exception):
    """This event is not stateful and cannot be paired with other events."""

    pass


class SerializationError(TypeError):
    """Cannot (de)serialize data."""

    pass
