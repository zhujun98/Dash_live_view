"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
from abc import ABC, abstractmethod
from collections import deque

import dash

from .application import application, Config, server
from .receiver import ReceiverFactory


class DashAppBase(ABC):
    """Base class for implementing a concrete app."""
    __default_config = {
        "pathname": "",
        "update_interval": 1.0,  # page update interval (s)
        "local": "tcp://*:*",  # TCP address of the test server
        "remote": "tcp://*:*",  # TCP address of the production server
    }

    def __init__(self, config):
        """Initialization.

        :param dict config: the default configuration.
        """
        self._parent = application

        self.config = Config()
        self.config.update(self.__default_config)
        self.config.update(config)

        self._data = None
        self._queue = deque(maxlen=1)

        # There are three "pathname"s:
        #     url_base_pathname,
        #     routes_pathname_prefix,
        #     requests_pathname_prefix
        #
        # `requests_pathname_prefix` is the prefix for the AJAX calls that
        # originate from the client (the web browser) and `routes_pathname_
        # prefix` is the prefix for the API routes on the backend (this flask
        # server). `url_base_pathname` will set `requests_pathname_prefix` and
        # `routes_pathname_prefix` to the same value.

        url_base_pathname = self.config.pathname
        # url_base_pathname must end with '/'
        if not url_base_pathname:
            url_base_pathname = "/"
        else:
            url_base_pathname = f"/{url_base_pathname}/"

        app = dash.Dash(__name__,
                        server=server,
                        url_base_pathname=url_base_pathname)

        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.config['suppress_callback_exceptions'] = True

        self._app = app
        self.register_callbacks(app)
        self.set_layout(app)

    @abstractmethod
    def register_callbacks(self, app):
        pass

    @abstractmethod
    def set_layout(self, app):
        pass

    def _update(self):
        """Update the current data.

        The method tries to grab data from the pipeline queue and then
        preprocess the data.
        """
        try:
            data = self._queue.popleft()
            self._data = self.preprocess_data(data)
        except IndexError:
            pass

    def preprocess_data(self, orig_data):
        """A hook for user-defined data pre-processing."""
        return orig_data

    def recv(self, test=False):
        """Receive data from the server.

        Bind to the data server and start the daemon receiver thread.
        """
        if test:
            endpoint = self.config.local
        else:
            endpoint = self.config.remote

        receiver = ReceiverFactory.create(self._parent.config.api,
                                          self._queue,
                                          endpoint)
        receiver.daemon = True
        receiver.start()

    def simulated_data(self):
        """A generator used for test."""
        yield
