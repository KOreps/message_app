# -*- coding: utf-8 -*-
from tornado import web, websocket, gen, httpserver
from tornadoredis.pubsub import BaseSubscriber
from tornadoredis import Client as RedisClient


class RedisSubscriber(BaseSubscriber):

    def on_message(self, msg):
        if msg.kind == 'message':
            subscribers = list(self.subscribers[msg.channel].keys())
            for s in subscribers:
                s.write_message(msg.body)
        elif msg.kind == 'disconnect':
            self.close()


class WebSocketHandler(websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        self.channels = []
        super(WebSocketHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):
        self.channels = ['users']
        application.redis_subscriber.subscribe(self.channels, self)


    def on_message(self, message):
        pass

    def on_close(self):
        for channel in self.channels:
            application.redis_subscriber.unsubscribe(channel, self)


class Application(web.Application):
    def __init__(self):
        self.redis_client = RedisClient()
        self.redis_subscriber = RedisSubscriber(self.redis_client)
        handlers = ((r'/', WebSocketHandler),)
        web.Application.__init__(self, handlers)


application = Application()
