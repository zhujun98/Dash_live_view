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
            "host": "localhost",
            "port": 8050,
            "test": False,
        })

    def run(self, applications, host='localhost', port=8050, *, test=False):
        cache.clear()

        sender = None
        try:
            if test:
                # start a simulated server in case of test
                sender = SimulatedServer(self)
                for app in applications:
                    app_port = app.config.local.split(":")[-1]
                    sender.generators[app_port] = app.simulated_data()
                sender.start()

            # start the receivers of all the applications
            for app in applications:
                app.recv(test=test)

            # run the development server implemented in Flask
            server.run(host=host, port=port)
        finally:
            if sender is not None and sender.is_alive():
                sender.terminate()


application = Application()


@server.route('/')
def home():
    return render_template("home.html")


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@server.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
