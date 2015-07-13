from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.python import log
from twisted.internet import reactor

import csv
import json
import random
import sys

__author__ = 'rostyslavfedynyshyn'


def sleep(delay):
    d = Deferred()
    reactor.callLater(delay, d.callback, None)
    return d


def read_text_file():
    with open('./../../../names.tsv', 'rb') as csv_file:
        peoples = csv.reader(csv_file, delimiter='\t')
        names_set = set([name[0] for name in peoples])

    return list(names_set)


class LeaderBoardLoadGeneratorClient(WebSocketClientProtocol):
    def __init__(self):
        self.server_path = 'ws://localhost:9000'
        self.names = read_text_file()

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    @inlineCallbacks
    def onOpen(self):
        print("WebSocket connection open.")

        while True:
            self.sendMessage(self.submit_random_score())
            yield sleep(0.5)

    def onClose(self, was_clean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def submit_random_score(self):
        choice_index = int(random.gauss(len(self.names) / 2, len(self.names) / 4))

        choice_index = max(0, choice_index)
        choice_index = min(len(self.names) - 1, choice_index)

        name = self.names[choice_index]
        score = random.randint(0, 100)
        request = json.dumps({"name": name, "score": score})

        print type(request), request
        return request


def main():
    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://localhost:9000/add", debug=False)
    factory.protocol = LeaderBoardLoadGeneratorClient

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()


if __name__ == "__main__":
    main()

