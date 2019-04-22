"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
import dash
import flask
from flask_caching import Cache


class Manager:
    __instance = None

    __apps = {}

    def __new__(cls, *args, **kwargs):
        """Create a singleton."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self._server = flask.Flask(__name__)

        self._cache = Cache(self._server, config={
            'CACHE_TYPE': 'filesystem',
            'CACHE_DIR': 'cache-directory',
            'CACHE_THRESHOLD': 100,
        })

    @property
    def flask_server(self):
        return self._server

    @property
    def cache(self):
        return self._cache

    def add_app(self, name):
        app = dash.Dash(name,
                        server=self._server,
                        sharing=True,
                        url_base_pathname=f"/{name}/")

        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.config['suppress_callback_exceptions'] = True

        # bookkeeping app
        self.__apps[name] = app

        return app

    def run_server(self, port=None, debug=None, host=None):
        self._cache.clear()
        self._server.run(port=port, debug=debug, host=host)
