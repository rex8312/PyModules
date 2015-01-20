#-*- coding: utf-8 -*-

__author__ = 'rex8312'

import logging

from tornado.concurrent import Future


class MessageBuffer(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, cursor=None):
        result_future = Future()
        if cursor:
            new_count = 0
            # new_count 찾는게 목적
            for msg in reversed(self.cache):
                if msg['id'] == cursor:
                    break
                new_count += 1
            #
            if new_count:
                result_future.set_result(self.cache[-new_count])
                return result_future
        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        future.set_result([])

    def new_messages(self, messages):
        logging.info('Sending new message to %r listeners', len(self.waiters))
        for future in self.waiters:
            future.set_result(messages)
        self.waiters = set()
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]