import json
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import redis

__author__ = 'rostyslavfedynyshyn'


class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        request_params = json.loads(payload)
        name = request_params["name"]
        score = request_params["score"]
        redis_client.zincrby('leaderboard', value=name, amount=score)
        print("Text message received: {0}".format(payload))

        redis_result = redis_client.zrevrange('leaderboard', 0, 20, withscores=True)
        print redis_result

        normalized_result = [(name.decode("utf-8"), int(score)) for name, score in redis_result]
        print normalized_result
        response = json.dumps(normalized_result)
        self.sendMessage(response, isBinary)


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
