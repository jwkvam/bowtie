"""Authentication out of the box.

References
----------
https://stackoverflow.com/questions/13428708/best-way-to-make-flask-logins-login-required-the-default
https://stackoverflow.com/questions/14367991/flask-before-request-add-exception-for-specific-route

"""

from typing import Dict, Optional
from abc import ABC, abstractmethod

from flask import Response, request, session

from bowtie._app import App


class Auth(ABC):
    """Abstract Authentication class."""

    def __init__(self, app: App) -> None:
        """Create Auth class to protect flask routes and socketio connect."""
        self.app = app
        self.app.app.before_request(self.before_request)
        # only need to check credentials on "connect" event
        self.app._socketio.on('connect')(self.socketio_auth)  # pylint: disable=protected-access

    @abstractmethod
    def before_request(self):
        """Determine if a user is allowed to view this route.

        Name is subject to change.

        Returns
        -------
        None, if no protection is needed.

        """

    @abstractmethod
    def socketio_auth(self) -> bool:
        """Determine if a user is allowed to establish socketio connection.

        Name is subject to change.
        """


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

    def before_request(self) -> Optional[Response]:
        """Determine if a user is allowed to view this route."""
        auth = request.authorization
        if not auth or not self._check_auth(auth.username, auth.password):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        session['logged_in'] = auth.username
        # pylint wants this return statement
        return None
