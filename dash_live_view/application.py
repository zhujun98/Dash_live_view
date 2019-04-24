"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
from flask import Flask
from flask_caching import Cache

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

    def run(self, applications, host='localhost', port=8050):
        cache.clear()

        for app in applications:
            app.recv()

        server.run(host, port)


application = Application()
