import time
from threading import Thread


class ReceiverFactory:

    class EuXFELReceiver(Thread):
        def __init__(self, data_queue, address):
            """Initialization.

            :param deque data_queue: a deque to store train data.
            :param str address: TCP address of the server.
            """
            super().__init__()

            self._queue = data_queue
            self._address = address

            self._running = False

        def run(self):
            """Receiving data from a Karabo bridge."""
            self._running = True

            from karabo_bridge import Client

            with Client(self._address, timeout=1) as client:
                print(f"Binding to server: {self._address}!")
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
            # TODO: assign default api
            raise ValueError("Not understandable api!")

        if api.lower() == "euxfel":
            return cls.EuXFELReceiver(*args, **kwargs)
