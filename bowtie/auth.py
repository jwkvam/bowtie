"""Authentication out of the box.

References
----------
https://stackoverflow.com/questions/13428708/best-way-to-make-flask-logins-login-required-the-default
"""

from typing import Dict, Callable
from abc import ABC, abstractmethod
from functools import wraps

from flask import Response, request, session

from bowtie._app import App


class Auth(ABC):
    """Abstract Authentication class."""

    def __init__(self, app: App) -> None:
        """Create Auth class to protect flask routes and socketio connect."""
        self.app = app
        self._protect_routes()
        # only need to check credentials on "connect" event
        self.app._socketio.on('connect')(self.socketio_auth)  # pylint: disable=protected-access

    def _protect_routes(self) -> None:
        """Protect flask routes with authentication."""
        # TODO all routes? what about index for logins if not basic auth
        # for name, method in self.app.app.view_functions.items():
        #     # if view_name != self._index_view_name:
        #     self.app.app.view_functions[name] = self.requires_auth(method)
        @self.app.app.before_request
        def access():
            return self.before_request()

    @abstractmethod
    def requires_auth(self, func: Callable) -> Callable:
        """Determine if a user is allowed to view this route.

        Name is subject to change.
        """
        pass

    @abstractmethod
    def before_request(self):
        """Determine if a user is allowed to view this route.

        Name is subject to change.
        """
        pass

    @abstractmethod
    def socketio_auth(self) -> bool:
        """Determine if a user is allowed to establish socketio connection.

        Name is subject to change.
        """
        pass


class BasicAuth(Auth):
    """Basic Authentication."""

    def __init__(self, app: App, credentials: Dict[str, str]) -> None:
        """
        Create basic auth with credentials.

        Parameters
        ----------
        credentials : dict
            Usernames and passwords should be passed in as a dictionary.

        Examples
        --------
        >>> from bowtie import App
        >>> from bowtie.auth import BasicAuth
        >>> app = App(__name__)
        >>> auth = BasicAuth(app, {'alice': 'secret1', 'bob': 'secret2'})

        """
        self.credentials = credentials
        super().__init__(app)

    def _check_auth(self, username: str, password: str) -> bool:
        """Check if a username/password combination is valid."""
        try:
            return self.credentials[username] == password
        except KeyError:
            return False

    def socketio_auth(self) -> bool:
        """Determine if a user is allowed to establish socketio connection."""
        try:
            return session['logged_in'] in self.credentials
        except KeyError:
            return False

    def before_request(self):
        """Determine if a user is allowed to view this route."""
        auth = request.authorization
        if not auth or not self._check_auth(auth.username, auth.password):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        session['logged_in'] = auth.username

    def requires_auth(self, func: Callable) -> Callable:
        """Determine if a user is allowed to view this route."""
        @wraps(func)
        def decorator(*args, **kargs):
            value = self.before_request()
            if value is None:
                return func(*args, **kargs)
            return value
        return decorator
