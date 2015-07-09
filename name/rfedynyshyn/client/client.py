from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.python import log
from twisted.internet import reactor

import sys

__author__ = 'rostyslavfedynyshyn'

def sleep(delay):
    d = Deferred()
    reactor.callLater(delay, d.callback, None)
    return d


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    @inlineCallbacks
    def onOpen(self):
        print("WebSocket connection open.")

        # start sending messages every second ..
        while True:
            self.sendMessage(u"1".encode('utf8'))
            yield sleep(5)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, was_clean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))



if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://localhost:9000", debug=False)
    factory.protocol = MyClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()