import json
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import redis
from twisted.web.client import getPage

__author__ = 'rostyslavfedynyshyn'


class MyServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):

        if self.http_request_path == '/add':
            self.add_scores(payload)
        elif self.http_request_path == '/top':
            self.get_top_n_players(payload)

    def get_top_n_players(self, payload):
        request_params = json.loads(payload)
        number = request_params["number"]

        redis_result = self.redis_client.zrevrange('leaderboard', 0, int(number) - 1, withscores=True)

        normalized_result = [(name.decode("utf-8"), int(score)) for name, score in redis_result]
        response = json.dumps(normalized_result)

        self.sendMessage(response, isBinary=False)

    def add_scores(self, payload):
        request_params = json.loads(payload)
        name = request_params["name"]
        score = request_params["score"]
        self.redis_client.zincrby('leaderboard', value=name, amount=score)
        print("Text message received: {0}".format(payload))

    def onClose(self, was_clean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()
