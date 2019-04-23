from collections import deque

from flask_caching import Cache


class DashApp:
    def __init__(self, dash_app, server):
        self._app = dash_app

        self._queue = deque(maxlen=1)

        self._cache = Cache(server, config={
            'CACHE_TYPE': 'filesystem',
            'CACHE_DIR': 'cache-directory',
            'CACHE_THRESHOLD': 100,
        })

        self._daq = None

    @property
    def app(self):
        return self._app

    @property
    def cache(self):
        return self._cache

    @property
    def queue(self):
        return self._queue

    @property
    def daq(self):
        return self._daq

    @daq.setter
    def daq(self, v):
        self._daq = v
