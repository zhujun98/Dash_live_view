"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
import dash
from flask import Flask

from .dash_app import DashApp


class Manager:
    __instance = None

    __apps = {}

    def __new__(cls, *args, **kwargs):
        """Create a singleton."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self._server = Flask(__name__)

    @property
    def server(self):
        return self._server

    def new_app(self, name, url_base_pathname=None):
        if url_base_pathname is None:
            url_base_pathname = name

        # url_base_pathname must end with '/'
        if not url_base_pathname:
            url_base_pathname = "/"
        else:
            url_base_pathname = f"/{url_base_pathname}/"

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
        app = dash.Dash(name,
                        server=self._server,
                        url_base_pathname=url_base_pathname)

        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.config['suppress_callback_exceptions'] = True

        # bookkeeping dash_app
        self.__apps[url_base_pathname] = DashApp(app, self._server)

        return self.__apps[url_base_pathname]

    def run(self, hostname='localhost', port=8050):
        self.run_daq()
        self._server.run(hostname, port)

    def run_daq(self):
        for app in self.__apps.values():
            app.daq.start()
