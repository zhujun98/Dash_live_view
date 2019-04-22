"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
import dash
import flask
from flask_caching import Cache
from werkzeug.wsgi import DispatcherMiddleware


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

    def new_dash_app(self, name, requests_pathname=None):
        if requests_pathname is None:
            requests_pathname = name

        # requests_pathname must end with '/'
        if not requests_pathname:
            requests_pathname = "/"
            pathname = "/"  # key used in bookkeeping app instance
        else:
            requests_pathname = f"/{requests_pathname}/"
            pathname = requests_pathname[:-1]  # strip the last "/"

        app = dash.Dash(name, requests_pathname_prefix=requests_pathname)

        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.config['suppress_callback_exceptions'] = True

        # bookkeeping app
        self.__apps[pathname] = app

        return app

    @property
    def application(self):
        """Return an application object.

        The application object can be run as a WSGI app like so
        $ gunicorn wsgi:application
        or passed as an argument to the Werkzeug development server like so
        $ from werkzeug.serving import run_simple
        $ run_simple('localhost', 8050, application)
        """
        self._cache.clear()

        return DispatcherMiddleware(self._server, {
            pathname: app.server for (pathname, app) in self.__apps.items()
        })
