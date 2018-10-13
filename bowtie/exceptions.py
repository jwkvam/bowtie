"""Bowtie exceptions."""


class YarnError(Exception):
    """Errors from ``Yarn``."""


class WebpackError(Exception):
    """Errors from ``Webpack``."""


class SizeError(Exception):
    """Size values must be a number."""


class GridIndexError(IndexError):
    """Invalid index into the grid layout."""


class NoUnusedCellsError(Exception):
    """All cells are used."""


class SpanOverlapError(Exception):
    """Spans may not overlap."""


class MissingRowOrColumn(Exception):
    """Missing a row or column."""


class NoSidebarError(Exception):
    """Cannot add to the sidebar when it doesn't exist."""


class NotStatefulEvent(Exception):
    """This event is not stateful and cannot be paired with other events."""


class SerializationError(TypeError):
    """Cannot serialize the data for command."""
