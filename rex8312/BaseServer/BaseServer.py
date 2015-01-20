#-*- coding: utf-8 -*-

__author__ = 'rex8312'


import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
import os.path
import uuid
import json

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

define('port', default=8888, help='run on the given port', type=int)
define('debug', default=False, help='run in debug mode')


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie('chatdemo_user')
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        import random
        data = random.random()
        self.write(json.dumps({'succ': True, 'data': data}))


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def get_compression_options(self):
        return {}

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size]

    @classmethod
    def send_updates(cls, chat):
        logging.info('sending messages to %d waiters', len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error('error sending message', exc_info=True)

    def on_message(self, message):
        logging.info('get message %r', message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            'id': str(uuid.uuid4()),
            'body': parsed['body'],
        }
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            #login_url='/auth/login',
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()