"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
from flask import Flask

server = Flask(__name__)


def run_all(applications, host='localhost', port=8050):
    server.run(host, port)
