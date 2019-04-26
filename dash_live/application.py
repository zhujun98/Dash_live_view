"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
from flask import Flask, render_template, request
from flask_caching import Cache

from .sender import SimulatedServer


server = Flask(__name__)

cache = Cache(server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',
    'CACHE_THRESHOLD': 100,
})


class Config(dict):
    """Project configuration."""
    def __init__(self):
        super().__init__()

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)


class Application:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            return super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.config = Config()
        self.config.update({
            "api": None,
            "title": "app",
            "host": "localhost",
            "port": 8050,
            "test": False,
        })

        self._pathnames = []  # app pathnames

    @property
    def pathnames(self):
        return self._pathnames

    def run(self, applications, host='localhost', port=8050, *,
            test=False, mock=True):
        cache.clear()

        sender = None
        try:
            if test and mock:
                # start a simulated server in case of test with mocking data
                sender = SimulatedServer(self)
                for app in applications:
                    app_port = app.config.local.split(":")[-1]
                    sender.generators[app_port] = app.simulated_data()
                sender.start()

            # start the receivers of all the applications
            for app in applications:
                self._pathnames.append(app.config.pathname)
                if test:
                    endpoint = app.config.local
                else:
                    endpoint = app.config.remote

                app.recv(endpoint)

            # run the development server implemented in Flask
            server.run(host=host, port=port)
        finally:
            if sender is not None and sender.is_alive():
                sender.terminate()


application = Application()


@server.route('/')
def home():
    pathnames = application.pathnames
    # TODO: replace the dirty hack
    pathnames.extend([""]*3)
    return render_template("home.html",
                           title=application.config.title,
                           pathname1=pathnames[0],
                           pathname2=pathnames[1],
                           pathname3=pathnames[2],
    )


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@server.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
