# -*- coding: utf-8 -*-
"""Control components."""

from collections import Iterable

from bowtie._component import Component, jdumps


def _jsbool(x):
    """Convert Python bool to Javascript bool."""
    return repr(x).lower()


# pylint: disable=too-few-public-methods
class _Controller(Component):
    """Abstract class all control components inherit.

    Used to test if a an object is a controller.
    """

    pass


class Button(_Controller):
    """An Ant design button."""

    _TEMPLATE = 'button.jsx'
    _COMPONENT = 'SimpleButton'
    _PACKAGE = None
    _TAG = ('<SimpleButton '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            'label={{{label}}} '
            '/>')

    def __init__(self, label='', caption=''):
        """Create a button.

        Parameters
        ----------
        label : str, optional
            Label on the button.
        caption : str, optional
            Heading text.
        """
        super(Button, self).__init__()

        self._instantiate = self._TAG.format(
            label="'{}'".format(label),
            uuid="'{}'".format(self._uuid)
        )
        self.caption = caption

    def on_click(self):
        """Emit an event when the button is clicked.

        | **Payload:** ``None``.

        Returns
        -------
        str
            Name of click event.

        """
        pass


class Dropdown(_Controller):
    """Dropdown based on react-select."""

    _TEMPLATE = 'dropdown.jsx'
    _COMPONENT = 'Dropdown'
    _PACKAGE = 'react-select@1.0.0-rc.3'
    _TAG = ('<Dropdown initOptions={{{options}}} '
            'multi={{{multi}}}'
            'default={{{default}}}'
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, labels=None, values=None, multi=False, default=None, caption=''):
        """Create a drop down.

        Parameters
        ----------
        labels : array-like, optional
            List of strings which will be visible to the user.
        values : array-like, optional
            List of values associated with the labels that are hidden from the user.
        multi : bool, optional
            If multiple selections are allowed.
        caption : str, optional
            Heading text.

        """
        super(Dropdown, self).__init__()

        if labels is None and values is None:
            labels = []
            values = []

        options = [dict(value=value, label=str(label)) for value, label in zip(values, labels)]

        self._instantiate = self._TAG.format(
            options=jdumps(options),
            multi='true' if multi else 'false',
            default=jdumps(default),
            uuid="'{}'".format(self._uuid)
        )
        self.caption = caption

    def on_change(self):
        """Emit an event when the selection changes.

        | **Payload:** ``dict`` with keys "value" and "label".

        """
        return self.get

    # pylint: disable=no-self-use
    def do_options(self, labels, values):
        """Replace the drop down fields.

        Parameters
        ----------
        labels : array-like
            List of strings which will be visible to the user.
        values : array-like
            List of values associated with the labels that are hidden from the user.

        Returns
        -------
        None

        """
        return [dict(label=l, value=v) for l, v in zip(labels, values)]

    # pylint: disable=no-self-use
    def do_choose(self, values):
        """Replace the drop down fields.

        Parameters
        ----------
        values : list or str or int
            Value(s) of drop down item(s) to be selected.

        Returns
        -------
        None

        """
        return values

    def get(self, data):
        """Return selected value(s)."""
        return data


class Switch(_Controller):
    """Toggle switch."""

    _TEMPLATE = 'switch.jsx'
    _COMPONENT = 'Toggle'
    _PACKAGE = 'antd'
    _TAG = ('<Toggle '
            'defaultChecked={{{defaultChecked}}} '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, initial=False, caption=''):
        """Create a toggle switch.

        Parameters
        ----------
        initial : bool, optional
            Starting state of the switch.
        caption : str, optional
            Label appearing above the widget.

        """
        super(Switch, self).__init__()
        self._instantiate = self._TAG.format(
            uuid="'{}'".format(self._uuid),
            defaultChecked=_jsbool(initial)
        )
        self.caption = caption

    def on_switch(self):
        """Emit an event when the switch is toggled.

        | **Payload:** ``bool`` status of the switch.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    # pylint: disable=no-self-use
    def get(self, data):
        """
        Get the state of the switch.

        Returns
        -------
        bool
            True if the switch is enabled.
        """
        return data


class _DatePickers(_Controller):
    """Specific Date Pickers inherit this class."""

    _TEMPLATE = 'date.jsx'
    _COMPONENT = 'PickDates'
    _PACKAGE = 'antd'
    _TAG = ('<PickDates '
            'date={{{date_type}}} '
            'month={{{month_type}}} '
            'range={{{range_type}}} '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, date_type=False, month_type=False, range_type=False,
                 caption=''):
        super(_DatePickers, self).__init__()
        self._instantiate = self._TAG.format(
            uuid="'{}'".format(self._uuid),
            date_type=_jsbool(date_type),
            month_type=_jsbool(month_type),
            range_type=_jsbool(range_type)
        )
        self.caption = caption


class DatePicker(_DatePickers):
    """A Date Picker.

    Let's you choose an individual day.
    """

    def __init__(self, caption=''):
        """Create a date picker.

        Parameters
        ----------
        caption : str, optional
            Heading text.

        """
        super(DatePicker, self).__init__(date_type=True, caption=caption)

    def on_change(self):
        """Emit an event when a date is selected.

        | **Payload:** ``str`` of the form ``"yyyy-mm-dd"``.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    # pylint: disable=no-self-use
    def get(self, data):
        """
        Get the currently selected date.

        Returns
        -------
        str
            Date in the format "YYYY-MM-DD"
        """
        return data


class MonthPicker(_DatePickers):
    """A Month Picker.

    Let's you choose a month and year.
    """

    def __init__(self, caption=''):
        """Create month picker.

        Parameters
        ----------
        caption : str, optional
            Heading text.

        """
        super(MonthPicker, self).__init__(month_type=True, caption=caption)

    def on_change(self):
        """Emit an event when a month is selected.

        | **Payload:** ``str`` of the form ``"yyyy-mm"``.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    # pylint: disable=no-self-use
    def get(self, data):
        """
        Get the currently selected month.

        Returns
        -------
        str
            Month in the format "YYYY-MM"
        """
        return data


class RangePicker(_DatePickers):
    """A Date Range Picker.

    Choose two dates to use as a range.
    """

    def __init__(self, caption=''):
        """Create a date range picker.

        Parameters
        ----------
        caption : str, optional
            Heading text.

        """
        super(RangePicker, self).__init__(range_type=True, caption=caption)

    def on_change(self):
        """Emit an event when a range is selected.

        | **Payload:** ``list`` of two dates ``["yyyy-mm-dd", "yyyy-mm-dd"]``.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    # pylint: disable=no-self-use
    def get(self, data):
        """
        Get the currently selected date range.

        Returns
        -------
        list
            A list of two strings ``["yyyy-mm-dd", "yyyy-mm-dd"]``.
        """
        return data


class Number(_Controller):
    """A number input widget with increment and decrement buttons.

    References
    ----------
    https://ant.design/components/input/

    """

    _TEMPLATE = 'number.jsx'
    _COMPONENT = 'AntNumber'
    _PACKAGE = 'antd'
    _TAG = ('<AntNumber '
            'start={{{start}}} '
            'min={{{minimum}}} '
            'max={{{maximum}}} '
            'step={{{step}}} '
            'size={{{size}}} '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, start=0, minimum=-1e100, maximum=1e100,
                 step=1, size='default', caption=''):
        """Create a number input.

        Parameters
        ----------
        start : number, optional
            Starting number
        minimum : number, optional
            Lower bound
        maximum : number, optional
            Upper bound
        size : 'default', 'large', 'small', optional
            Size of the textbox.
        caption : str, optional
            Heading text.
        """
        super(Number, self).__init__()
        self._instantiate = self._TAG.format(
            uuid="'{}'".format(self._uuid),
            start=start,
            minimum=minimum,
            maximum=maximum,
            step=step,
            size="'{}'".format(size)
        )
        self.caption = caption

    def on_change(self):
        """Emit an event when the number is changed.

        | **Payload:** ``number``

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    # pylint: disable=no-self-use
    def get(self, data):
        """
        Get the current number.

        Returns
        -------
        number

        """
        return data


class Textbox(_Controller):
    """A single line text box.

    References
    ----------
    https://ant.design/components/input/

    """

    _TEMPLATE = 'textbox.jsx'
    _COMPONENT = 'Textbox'
    _PACKAGE = 'antd'
    _TAG = ('<Textbox '
            'placeholder={{{placeholder}}} '
            'size={{{size}}} '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, placeholder='Enter text', size='default', caption=''):
        """Create a textbox.

        Parameters
        ----------
        placeholder : str, optional
            Initial text that appears.
        size : 'default', 'large', 'small', optional
            Size of the textbox.
        caption : str, optional
            Heading text.

        """
        super(Textbox, self).__init__()

        self._instantiate = self._TAG.format(
            uuid="'{}'".format(self._uuid),
            placeholder="'{}'".format(placeholder),
            size="'{}'".format(size)
        )
        self.caption = caption

    def on_enter(self):
        """Emit an event when enter is pressed in the textbox.

        | **Payload:** ``str``

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    def on_change(self):
        """Emit an event when the text is changed.

        | **Payload:** ``str``

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    # pylint: disable=no-self-use
    def get(self, data):
        """
        Get the current text.

        Returns
        -------
        str

        """
        return data


class Slider(_Controller):
    """Ant Design slider.

    References
    ----------
    https://ant.design/components/slider/

    """

    _TEMPLATE = 'slider.jsx'
    _COMPONENT = 'AntSlider'
    _PACKAGE = 'antd'
    _TAG = ('<AntSlider '
            'range={{{range}}} '
            'min={{{minimum}}} '
            'max={{{maximum}}} '
            'step={{{step}}} '
            'start={{{start}}} '
            'marks={{{marks}}} '
            'socket={{socket}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, start=None, ranged=False, minimum=0, maximum=100, step=1,
                 caption=''):
        """Create a slider.

        Parameters
        ----------
        start : number or list with two values, optional
            Determines the starting value.
            If a list of two values are given it will be a range slider.
        ranged : bool, optional
            If this is a range slider.
        minimum : number, optional
            Minimum value of the slider.
        maximum : number, optional
            Maximum value of the slider.
        step : number, optional
            Step size.
        caption : str, optional
            Heading text.

        """
        super(Slider, self).__init__()

        if not start:
            start = [0, 0] if ranged else 0
        elif isinstance(start, Iterable):
            start = list(start)
            ranged = True

        self._instantiate = self._TAG.format(
            uuid="'{}'".format(self._uuid),
            range=_jsbool(ranged),
            minimum=minimum,
            maximum=maximum,
            start=start,
            step=step,
            marks={minimum: str(minimum), maximum: str(maximum)}
        )
        self.caption = caption

    def on_change(self):
        """Emit an event when the slider's value changes.

        | **Payload:** ``number`` or ``list`` of values.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    def on_after_change(self):
        """Emit an event when the slider control is released.

        | **Payload:** ``number`` or ``list`` of values.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    # pylint: disable=no-self-use
    def get(self, data):
        """
        Get the currently selected value(s).

        Returns
        -------
        list or number
            List if it's a range slider and gives two values.
        """
        return data


class Nouislider(_Controller):
    """A lightweight JavaScript range slider library.

    Parameters
    ----------
    start : number or list with two values, optional
        Determines the starting value.
        If a list of two values are given it will be a range slider.
    minimum : number, optional
        Minimum value of the slider.
    maximum : number, optional
        Maximum value of the slider.
    tooltips : bool, optional
        Show a popup text box.
    caption : str, optional
        Heading text.

    References
    ----------
    https://refreshless.com/nouislider/events-callbacks/

    """

    _TEMPLATE = 'nouislider.jsx'
    _COMPONENT = 'Nouislider'
    _PACKAGE = 'nouislider@9.2.0'
    _TAG = ('<Nouislider range={{{{min: {min}, max: {max}}}}} '
            'socket={{socket}} '
            'start={{{start}}} '
            'tooltips={{{tooltips}}} '
            'uuid={{{uuid}}} '
            '/>')

    def __init__(self, start=0, minimum=0, maximum=100, tooltips=True, caption=''):
        """Create a slider."""
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
        """Emit an event when the slider is moved.

        https://refreshless.com/nouislider/events-callbacks/

        | **Payload:** ``list`` of values.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    def on_slide(self):
        """Emit an event when the slider is moved.

        https://refreshless.com/nouislider/events-callbacks/

        | **Payload:** ``list`` of values.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    def on_set(self):
        """Emit an event when the slider is moved.

        https://refreshless.com/nouislider/events-callbacks/

        | **Payload:** ``list`` of values.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    def on_change(self):
        """Emit an event when the slider is moved.

        https://refreshless.com/nouislider/events-callbacks/

        | **Payload:** ``list`` of values.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    def on_start(self):
        """Emit an event when the slider is moved.

        https://refreshless.com/nouislider/events-callbacks/

        | **Payload:** ``list`` of values.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    def on_end(self):
        """Emit an event when the slider is moved.

        https://refreshless.com/nouislider/events-callbacks/

        | **Payload:** ``list`` of values.

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    # pylint: disable=no-self-use
    def get(self, data):
        """
        Get the currently selected value(s).

        Returns
        -------
        list or number
            List if it's a range slider and gives two values.
        """
        return data
