"""Control components."""

from typing import Callable, Optional, List, Union, Tuple
from collections import Iterable

from bowtie._component import Component, jdumps, jsbool


# pylint: disable=too-few-public-methods
class _Controller(Component):
    """Abstract class all control components inherit.

    Used to test if a an object is a controller.
    """

    # pylint: disable=abstract-method
    def __init__(self, caption: Optional[str] = None) -> None:
        super().__init__()
        self.caption = caption

    @property
    def _instantiate(self) -> str:
        tagwrap = '{component}' + self._tagbase
        return self._insert(tagwrap, self._comp)


class Button(_Controller):
    """An Ant design button."""

    _TEMPLATE = 'button.jsx'
    _COMPONENT = 'SimpleButton'
    _PACKAGE = None
    _ATTRS = "label={{'{label}'}}"

    def __init__(self, label: str = '', caption: Optional[str] = None) -> None:
        """Create a button.

        Parameters
        ----------
        label : str, optional
            Label on the button.
        caption : str, optional
            Heading text.

        """
        super().__init__(caption=caption)
        self._comp = self._tag.format(
            label=label
        )

    def on_click(self) -> None:
        """Emit an event when the button is clicked.

        | **Payload:** ``None``.

        Returns
        -------
        str
            Name of click event.

        """
        pass


class Link(_Controller):
    """An internal link.

    This doesn't create a page reload.
    """

    _TEMPLATE = 'link.jsx'
    _COMPONENT = 'ALink'
    _PACKAGE = None
    _ATTRS = "to={{'{link}'}}"

    def __init__(self, link: str = '/', caption: Optional[str] = None) -> None:
        """Create a button.

        Parameters
        ----------
        link : str

        """
        super().__init__(caption=caption)
        self._comp = self._tag.format(
            link=link
        )


class Upload(_Controller):
    """Draggable file upload widget."""

    _TEMPLATE = 'upload.jsx'
    _COMPONENT = 'AntUpload'
    _PACKAGE = None
    _ATTRS = "multiple={{{multiple}}}"

    def __init__(self, multiple=True, caption=None):
        """Create the widget.

        Note: the handler parameter may be changed in the future.

        Parameters
        ----------
        multiple : bool, optional
            If true, you can upload multiple files at once. Even with this set to true,
            the handler will get called once per file uploaded.
        caption : str, optional
            Heading text.

        """
        super().__init__(caption=caption)
        self._comp = self._tag.format(
            multiple=jsbool(multiple)
        )

    def on_upload(self):
        """Emit an event when the selection changes.

        | **Payload:** ``tuple`` with a str (name) and BytesIO (stream).

        The user is responsible for storing the object in this function
        if they want it for later use. To indicate an error, return True,
        otherwise a return value of None or False indicate success.

        """
        pass


class Dropdown(_Controller):
    """Dropdown based on react-select."""

    _TEMPLATE = 'dropdown.jsx'
    _COMPONENT = 'Dropdown'
    _PACKAGE = 'react-select@1.2.1'
    _ATTRS = ('initOptions={{{options}}} '
              'multi={{{multi}}} '
              'default={{{default}}}')

    def __init__(self, labels: Optional[List[str]] = None,
                 values: Optional[List[Union[str, int]]] = None, multi: bool = False,
                 default: Optional[Union[str, int]] = None, caption: Optional[str] = None) -> None:
        """Create a drop down.

        Parameters
        ----------
        labels : array-like, optional
            List of strings which will be visible to the user.
        values : array-like, optional
            List of values associated with the labels that are hidden from the user.
        multi : bool, optional
            If multiple selections are allowed.
        default : str or int, optional
            The default selected value.
        caption : str, optional
            Heading text.

        """
        super().__init__(caption=caption)

        if values is not None and labels is not None:
            options = [{'value': value, 'label': str(label)}
                       for value, label in zip(values, labels)]
        else:
            options = []

        self._comp = self._tag.format(
            options=jdumps(options),
            multi=jsbool(multi),
            default=jdumps(default),
        )

    def on_change(self) -> Callable:
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
    _PACKAGE = None
    _ATTRS = 'defaultChecked={{{defaultChecked}}}'

    def __init__(self, initial: bool = False, caption: Optional[str] = None) -> None:
        """Create a toggle switch.

        Parameters
        ----------
        initial : bool, optional
            Starting state of the switch.
        caption : str, optional
            Label appearing above the widget.

        """
        super().__init__(caption=caption)
        self._comp = self._tag.format(
            defaultChecked=jsbool(initial)
        )

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
    _PACKAGE = None
    _ATTRS = ('date={{{date_type}}} '
              'month={{{month_type}}} '
              'range={{{range_type}}}')

    def __init__(self, date_type: bool = False, month_type: bool = False, range_type: bool = False,
                 caption: Optional[str] = None) -> None:
        super().__init__(caption=caption)
        self._comp = self._tag.format(
            date_type=jsbool(date_type),
            month_type=jsbool(month_type),
            range_type=jsbool(range_type)
        )


class DatePicker(_DatePickers):
    """A Date Picker.

    Let's you choose an individual day.
    """

    def __init__(self, caption: Optional[str] = None) -> None:
        """Create a date picker.

        Parameters
        ----------
        caption : str, optional
            Heading text.

        """
        super().__init__(date_type=True, caption=caption)

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

    def __init__(self, caption: Optional[str] = None) -> None:
        """Create month picker.

        Parameters
        ----------
        caption : str, optional
            Heading text.

        """
        super().__init__(month_type=True, caption=caption)

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

    def __init__(self, caption: Optional[str] = None) -> None:
        """Create a date range picker.

        Parameters
        ----------
        caption : str, optional
            Heading text.

        """
        super().__init__(range_type=True, caption=caption)

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
    """A number input widget with increment and decrement buttons."""

    _TEMPLATE = 'number.jsx'
    _COMPONENT = 'AntNumber'
    _PACKAGE = None
    _ATTRS = ('start={{{start}}} '
              'min={{{minimum}}} '
              'max={{{maximum}}} '
              'step={{{step}}} '
              "size={{'{size}'}}")

    def __init__(self, start: int = 0, minimum: float = -1e100, maximum: float = 1e100,
                 step: int = 1, size: str = 'default', caption: Optional[str] = None) -> None:
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
            Size of the text box.
        caption : str, optional
            Heading text.

        References
        ----------
        https://ant.design/components/input/

        """
        super().__init__(caption=caption)
        self._comp = self._tag.format(
            start=start,
            minimum=minimum,
            maximum=maximum,
            step=step,
            size=size
        )

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
    """A single line text box."""

    _TEMPLATE = 'textbox.jsx'
    _COMPONENT = 'Textbox'
    _PACKAGE = None
    _ATTRS = ("placeholder={{'{placeholder}'}} "
              "size={{'{size}'}} "
              "type={{'{area}'}} "
              'autosize={{{autosize}}} '
              'disabled={{{disabled}}}')

    def __init__(self, placeholder: str = 'Enter text', size: str = 'default', area: bool = False,
                 autosize: bool = False, disabled: bool = False,
                 caption: Optional[str] = None) -> None:
        """Create a text box.

        Parameters
        ----------
        placeholder : str, optional
            Initial text that appears.
        size : 'default', 'large', 'small', optional
            Size of the text box.
        area : bool, optional
            Create a text area if True else create a single line input.
        autosize : bool, optional
            Automatically size the widget based on the content.
        disabled : bool, optional
            Disable input to the widget.
        caption : str, optional
            Heading text.

        References
        ----------
        https://ant.design/components/input/

        """
        super().__init__(caption=caption)

        self._comp = self._tag.format(
            area='textarea' if area else 'text',
            autosize=jsbool(autosize),
            disabled=jsbool(disabled),
            placeholder=placeholder,
            size=size
        )

    # pylint: disable=no-self-use
    def do_text(self, text):
        """Set the text of the text box.

        Parameters
        ----------
        text : str
            String of the text box.

        """
        return text

    def on_enter(self):
        """Emit an event when enter is pressed in the text box.

        | **Payload:** ``str``

        Returns
        -------
        str
            Name of event.

        """
        return self.get

    def on_change(self) -> Callable:
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
    """Ant Design slider."""

    _TEMPLATE = 'slider.jsx'
    _COMPONENT = 'AntSlider'
    _PACKAGE = None
    _ATTRS = ('range={{{range}}} '
              'min={{{minimum}}} '
              'max={{{maximum}}} '
              'step={{{step}}} '
              'start={{{start}}} '
              'marks={{{marks}}} '
              'vertical={{{vertical}}}')

    def __init__(self, start: Optional[Union[int, Tuple[int, int]]] = None, ranged: bool = False,
                 minimum: int = 0, maximum: int = 100, step: int = 1,
                 vertical: bool = False, caption: Optional[str] = None) -> None:
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
        vertical : bool, optional
            If True, the slider will be vertical
        caption : str, optional
            Heading text.

        References
        ----------
        https://ant.design/components/slider/

        """
        super().__init__(caption=caption)

        if not start:
            if ranged:
                start = minimum, maximum
            else:
                start = minimum
        elif isinstance(start, Iterable):
            start = list(start)
            ranged = True

        self._comp = self._tag.format(
            range=jsbool(ranged),
            minimum=minimum,
            maximum=maximum,
            start=start,
            step=step,
            marks={minimum: str(minimum), maximum: str(maximum)},
            vertical=jsbool(vertical)
        )

    # pylint: disable=no-self-use
    def do_max(self, value):
        """Replace the max value of the slider.

        Parameters
        ----------
        value : int
            Maximum value of the slider.

        """
        return value

    def do_min(self, value):
        """Replace the min value of the slider.

        Parameters
        ----------
        value : int
            Minimum value of the slider.

        """
        return value

    def do_value(self, value):
        """Set the value of the slider.

        Parameters
        ----------
        value : int
            Value of the slider.

        """
        return value

    def do_inc(self, value=1):
        """Increment value of slider by given amount.

        Parameters
        ----------
        value : int
            Number to change value of slider by.

        """
        return value

    def do_min_max_value(self, minimum, maximum, value):
        """Set the minimum, maximum, and value of slider simultaneously.

        Parameters
        ----------
        minimum : int
            Minimum value of the slider.
        maximum : int
            Maximum value of the slider.
        value : int
            Value of the slider.

        """
        return minimum, maximum, value

    def on_change(self) -> Callable:
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
    """A lightweight JavaScript range slider library."""

    _TEMPLATE = 'nouislider.jsx'
    _COMPONENT = 'Nouislider'
    _PACKAGE = 'nouislider@11.0.3'
    _ATTRS = ('range={{{{min: {min}, max: {max}}}}} '
              'socket={{socket}} '
              'start={{{start}}} '
              'tooltips={{{tooltips}}}')

    def __init__(self, start: Union[int, Tuple[int, int]] = 0, minimum: int = 0,
                 maximum: int = 100, tooltips: bool = True, caption: Optional[str] = None) -> None:
        """Create a slider.

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
        super().__init__(caption=caption)

        if not isinstance(start, Iterable):
            nstart = [start]
        else:
            nstart = list(start)
        self._comp = self._tag.format(
            min=minimum,
            max=maximum,
            start=nstart,
            tooltips=jsbool(tooltips)
        )

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

    def on_change(self) -> Callable:
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
