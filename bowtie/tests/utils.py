# -*- coding: utf-8 -*-
"""Utility functions for testing only."""

from bowtie._component import Component


def reset_uuid():
    """Reset the uuid counter for components."""
    # pylint: disable=protected-access
    Component._NEXT_UUID = 0
