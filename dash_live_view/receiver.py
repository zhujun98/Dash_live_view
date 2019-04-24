"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
import time
from threading import Thread


class ReceiverFactory:
    """Class Factory which produces receiver instance for different APIs."""
    # TODO: implement a base class

    class EuXFELReceiver(Thread):
        def __init__(self, data_queue, endpoint):
            """Initialization.

            :param deque data_queue: a deque to store train data.
            :param str endpoint: TCP address of the server.
            """
            super().__init__()

            self._queue = data_queue
            self._endpoint = endpoint

            self._running = False

        def run(self):
            """Receiving data from a Karabo bridge."""
            self._running = True

            from karabo_bridge import Client

            # TODO: make timeout configurable
            with Client(self._endpoint, timeout=1) as client:
                print(f"Binding to server: {self._endpoint}\n")
                while self._running:
                    t0 = time.perf_counter()
                    try:
                        self._queue.append(client.next())
                    except TimeoutError:
                        continue
                    print("Time for retrieving data from the server: {:.1f} ms".
                          format(1000 * (time.perf_counter() - t0)))

        def terminate(self):
            self._running = False

    @classmethod
    def create(cls, api, *args, **kwargs):
        if api is None:
            raise ValueError("Not understandable api!")

        if api.lower() == "euxfel":
            return cls.EuXFELReceiver(*args, **kwargs)
