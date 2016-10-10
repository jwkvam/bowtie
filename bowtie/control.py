# -*- coding: utf-8 -*-
"""
Control components
"""

from collections import Iterable

from bowtie._component import Component, jdumps


# pylint: disable=too-few-public-methods
class _Controller(Component):
    """
    Used to test if a an object is a controller.
    All controllers must inherit this class.
    """
    pass


class Button(_Controller):
    _TEMPLATE = 'button.jsx'
    _COMPONENT = 'SimpleButton'
    _PACKAGE = None
    _TAG = ('<SimpleButton '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            'label={{{label}}} '
            '/>')

    def __init__(self, label='', caption=''):
        super(Button, self).__init__()

        self._instantiate = self._TAG.format(
            label="'{}'".format(label),
            uuid="'{}'".format(self._uuid)
        )
        self.caption = caption

    def on_click(self):
        pass


class DropDown(_Controller):
    _TEMPLATE = 'dropdown.jsx'
    _COMPONENT = 'DropDown'
    _PACKAGE = 'react-select'
    _TAG = ('<DropDown initOptions={{{options}}} '
            'multi={{{multi}}}'
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '/>')


    def __init__(self, options, multi=False, caption=''):
        super(DropDown, self).__init__()

        # options = [dict(value=x, label=str(x)) for x in options]

        self._instantiate = self._TAG.format(
            options=jdumps(options),
            multi='true' if multi else 'false',
            uuid="'{}'".format(self._uuid)
        )
        self.caption = caption

    def on_change(self):
        pass

    def do_options(self, data):
        pass


class Nouislider(_Controller):
    _TEMPLATE = 'nouislider.jsx'
    _COMPONENT = 'Nouislider'
    _PACKAGE = 'nouislider'
    _TAG = ('<Nouislider range={{{{min: {min}, max: {max}}}}} '
            'socket={{socket}} '
            'start={{{start}}} '
            'tooltips={{{tooltips}}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, start=0, minimum=0, maximum=100, tooltips=True, caption=''):
        super(Nouislider, self).__init__()

        if not isinstance(start, Iterable):
            start = [start]
        else:
            start = list(start)
        self._instantiate = self._TAG.format(
            uuid="'{}'".format(self._uuid),
            min=minimum,
            max=maximum,
            start=start,
            tooltips='true' if tooltips else 'false'
        )
        self.caption = caption

    def on_update(self):
        pass

    def on_slide(self):
        pass

    def on_set(self):
        pass

    def on_change(self):
        pass

    def on_start(self):
        pass

    def on_en(self):
        pass
