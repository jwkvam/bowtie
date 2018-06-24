"""Bowtie cache functions."""

import flask
from flask_socketio import emit
import eventlet
from eventlet.queue import LightQueue
import msgpack

from bowtie._component import pack


def validate(key):
    """Check that the key is a string or bytestring.

    That's the only valid type of key.
    """
    if not isinstance(key, (str, bytes)):
        raise KeyError('Key must be of type str or bytes, found type {}'.format(type(key)))


# pylint: disable=too-few-public-methods
class _Cache:
    """Store data in the browser.

    This cache uses session storage so data will stay
    in the browser until the tab is closed.
    All data must be serializable, which means if the
    serialization transforms the data it won't be the same
    when it is fetched.

    Examples
    --------
    >>> from bowtie import cache
    >>> cache['a'] = True  # doctest: +SKIP
    >>> cache['a']  # doctest: +SKIP
    True
    >>> cache['b'] = np.arange(5)  # doctest: +SKIP
    >>> cache['b']  # doctest: +SKIP
    [1, 2, 3, 4, 5]

    """

    def __getitem__(self, key):
        """Load the value stored with the key.

        Parameters
        ----------
        key : str
            The key to lookup the value stored.

        Returns
        -------
        object
            The value if the key exists in the cache, otherwise None.

        """
        validate(key)
        signal = 'cache_load'
        event = LightQueue(1)
        if flask.has_request_context():
            emit(signal, {'data': pack(key)}, callback=event.put)
        else:
            sio = flask.current_app.extensions['socketio']
            sio.emit(signal, {'data': pack(key)}, callback=event.put)
        return msgpack.unpackb(bytes(event.get(timeout=10)), encoding='utf8')

    def __setitem__(self, key, value):
        """Store the key value pair.

        Parameters
        ----------
        key : str
            The key to determine where it's stored, you'll need this to load the value later.
        value : object
            The value to store in the cache.

        Returns
        -------
        None

        """
        validate(key)
        signal = 'cache_save'
        if flask.has_request_context():
            emit(signal, {'key': pack(key), 'data': pack(value)})
        else:
            sio = flask.current_app.extensions['socketio']
            sio.emit(signal, {'key': pack(key), 'data': pack(value)})
        eventlet.sleep()


# pylint: disable=invalid-name
cache = _Cache()
