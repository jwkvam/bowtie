# -*- coding: utf-8 -*-

from collections import namedtuple

from enum import Enum

from bowtie.component import Component

# from event import Event

import json


class Controller(Component):
    """
    Used to test if a an object is a controller.
    All controllers must inherit this class.
    """
    pass


class Button(Controller):
    template = 'button.jsx'
    component = 'SimpleButton'
    package = 'react-button'
    tag = ('<SimpleButton '
           'socket={{socket}} '
           'uuid={{{uuid}}} '
           'label={{{label}}} '
           '/>')

    def __init__(self, label=''):
        super(Button, self).__init__()

        self.instantiate = self.tag.format(
            label="'{}'".format(label),
            uuid="'{}'".format(self._uuid)
        )

    def on_click(self):
        pass


class DropDown(Controller):
    template = 'dropdown.jsx'
    component = 'DropDown'
    package = 'react-select'
    tag = ('<DropDown initOptions={{{options}}} '
           'name={{{name}}} '
           'multi={{{multi}}}'
           'socket={{socket}} '
           'uuid={{{uuid}}} '
           '/>')


    def __init__(self, name, options, multi=False):
        super(DropDown, self).__init__()

        # options = [dict(value=x, label=str(x)) for x in options]


        self.instantiate = self.tag.format(
            name="'{}'".format(name),
            options=json.dumps(options),
            multi='true' if multi else 'false',
            uuid="'{}'".format(self._uuid)
        )

    def on_change(self):
        pass

    def do_options(self, data):
        pass


class Nouislider(Controller):
    template = 'nouislider.jsx'
    component = 'Nouislider'
    package = 'react-nouislider'
    tag = ('<Nouislider range={{{{min: {min}, max: {max}}}}} '
           'socket={{socket}} '
           'start={{{start}}} {tooltips} '
           'uuid={{{uuid}}} '
           '/>')


           # 'onChange={{ function(x) {{socket.emit("{uuid}#change", x);}} }} '

    def __init__(self, start=0, minimum=0, maximum=100, tooltips=False):
        super(Nouislider, self).__init__()
        self.instantiate = self.tag.format(
            uuid="'{}'".format(self._uuid),
            min=minimum,
            max=maximum,
            start=start,
            tooltips='tooltips' if tooltips else ''
        )

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
