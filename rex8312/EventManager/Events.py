# -*-coding: utf-8 -*-

__author__ = 'rex8312'


class Event(object):
    def __init__(self):
        pass

    @property
    def name(self):
        return 'generic event'


class NullEvent(object):
    @property
    def name(self):
        return 'null event'


class TickEvent(Event):
    @property
    def name(self):
        return 'tick event'