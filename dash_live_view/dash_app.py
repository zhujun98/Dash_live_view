from collections import deque

import dash
from flask_caching import Cache

from .manager import server


class BaseDashApp:
    def __init__(self, config):
        self._update_interval = config.update_interval

        self._queue = deque(maxlen=1)

        self._cache = Cache(server, config={
            'CACHE_TYPE': 'filesystem',
            'CACHE_DIR': 'cache-directory',
            'CACHE_THRESHOLD': 100,
        })

        # self._daq = DataAcquisition(self._queue)

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

        url_base_pathname = config.pathname
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

    @property
    def cache(self):
        return self._cache

    @property
    def daq(self):
        return self._daq

    @daq.setter
    def daq(self, v):
        self._daq = v
