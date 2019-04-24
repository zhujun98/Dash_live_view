from collections import deque

import dash

from .application import application, Config, server
from .receiver import ReceiverFactory


class DashAppBase:
    __default_config = {
        "pathname": "",
        "update_interval": 1.0,  # page update interval (s)
        "local": "tcp://*:*",  # TCP address of the test server
        "remote": "tcp://*:*",  # TCP address of the production server
    }
    def __init__(self, config):

        self._parent = application
        self._config = Config()
        self._config.update(self.__default_config)
        self._config.update(config)

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

        url_base_pathname = self._config.pathname
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

    def register_callbacks(self, app):
        raise NotImplementedError

    def set_layout(self, app):
        raise NotImplementedError

    def _update_data(self):
        try:
            data = self._queue.popleft()
            return self.preprocess_data(data)
        except IndexError:
            return None

    def preprocess_data(self, orig_data):
        return orig_data

    def recv(self):
        if self._parent.config.test:
            addr = self._config.local
        else:
            addr = self._config.remote

        receiver = ReceiverFactory.create(self._parent.config.api,
                                          self._queue,
                                          addr)
        receiver.start()
