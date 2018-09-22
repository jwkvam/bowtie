"""Static HTML Components."""

from flask import Markup
from markdown import markdown

from bowtie._component import Component


# pylint: disable=too-few-public-methods
class _HTML(Component):
    """Abstract class for HTML components."""

    # pylint: disable=abstract-method
    @property
    def _instantiate(self) -> str:
        tagwrap = '{component}' + self._tagbase
        return self._insert(tagwrap, self._comp)


# pylint: disable=too-few-public-methods
class Markdown(_HTML):
    """Display Markdown."""

    _TEMPLATE = 'markdown.jsx'
    _COMPONENT = 'Markdown'
    _PACKAGE = None
    _ATTRS = "initial={{'{initial}'}}"

    def __init__(self, initial: str = '') -> None:
        """Create a Markdown widget.

        Parameters
        ----------
        initial : str, optional
            Default markdown for the widget.

        """
        super().__init__()
        self._comp = self._tag.format(
            initial=Markup(markdown(initial).replace('\n', '\\n'))
        )

    # pylint: disable=no-self-use
    def do_text(self, text):
        """Replace widget with this text.

        Parameters
        ----------
        test : str
            Markdown text as a string.

        Returns
        -------
        None

        """
        return Markup(markdown(text))

    def get(self, text):
        """Get the current text.

        Returns
        -------
        String of html.

        """
        return text


class Link(_HTML):
    """An internal link.

    This doesn't create a page reload.
    """

    _TEMPLATE = 'link.jsx'
    _COMPONENT = 'ALink'
    _PACKAGE = None
    _ATTRS = "to={{'{link}'}}"

    def __init__(self, link: str = '/') -> None:
        """Create a button.

        Parameters
        ----------
        link : str

        """
        super().__init__()
        self._comp = self._tag.format(
            link=link
        )


class Div(_HTML):
    """Div tag."""

    _TEMPLATE = 'div.jsx'
    _COMPONENT = 'Bowdiv'
    _PACKAGE = None
    _ATTRS = "initial={{'{initial}'}}"

    def __init__(self, text: str = '') -> None:
        """Create header text with a size.

        Parameters
        ----------
        text : str
            Text of the header tag.

        """
        super().__init__()
        self._comp = self._tag.format(
            initial=text
        )

    # pylint: disable=no-self-use
    def do_text(self, text):
        """Replace widget with this text.

        Parameters
        ----------
        test : str
            Markdown text as a string.

        Returns
        -------
        None

        """
        return text

    def get(self, text):
        """Get the current text.

        Returns
        -------
        String of html.

        """
        return text


class Header(_HTML):
    """Header tag."""

    _TEMPLATE = 'header.jsx'
    _COMPONENT = 'Bowhead'
    _PACKAGE = None
    _ATTRS = ("initial={{'{initial}'}} "
              'size={{{size}}}')

    def __init__(self, text: str = '', size: int = 1) -> None:
        """Create header text with a size.

        Parameters
        ----------
        text : str
            Text of the header tag.
        size : int
            Size of the header tag from 1 to 6.

        """
        super().__init__()
        if size not in range(1, 7):
            raise ValueError('Header size must be in [1..6], found {}.'.format(size))
        self._comp = self._tag.format(
            initial=text,
            size=size
        )

    # pylint: disable=no-self-use
    def do_text(self, text):
        """Replace widget with this text.

        Parameters
        ----------
        test : str
            Markdown text as a string.

        Returns
        -------
        None

        """
        return text

    def get(self, text):
        """Get the current text.

        Returns
        -------
        String of html.

        """
        return text
