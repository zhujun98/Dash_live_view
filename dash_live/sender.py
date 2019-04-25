"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
from multiprocessing import Process
import functools


class SimulatedServer(Process):
    def __init__(self, app, *args, **kwargs):
        """Initialization.

        :param Application app: dash_live_view application.
        """
        super().__init__(*args, **kwargs)

        self._app = app

        # {port: generator}
        self.generators = dict()

    def run(self):
        """Override."""
        if self._app.config.api == "euxfel":
            self._send_euxfel_data()
        else:
            raise ValueError("Unknown api!")

    def _send_euxfel_data(self):
        """Send out data using EuXFEL Karabo bridge protocol."""
        import zmq
        import msgpack
        from karabo_bridge.simulation import containize

        context = zmq.Context()
        sockets = []
        generators = []
        for port, generator in self.generators.items():
            socket = context.socket(zmq.REP)
            socket.setsockopt(zmq.LINGER, 0)
            socket.bind(f'tcp://*:{port}')
            print(f"Prepare to send data throught port: {port}")
            sockets.append(socket)
            generators.append(generator)

        serializer = functools.partial(msgpack.dumps, use_bin_type=True)

        try:
            while True:
                for socket, generator in zip(sockets, generators):
                    if socket.recv() == b'next':
                        train_data = next(generator)

                        # TODO: make version ('2.2') configurable
                        msg = containize(train_data, 'msgpack', serializer, '2.2')
                        socket.send_multipart(msg, copy=False)
                    else:
                        print('Not understandable request')
                        break
        except KeyboardInterrupt:
            print('\nStopped.')
        finally:
            for socket in sockets:
                socket.close()
            context.destroy()
