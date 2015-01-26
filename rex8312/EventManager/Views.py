__author__ = 'rex8312'

from random import random


class RandomNumberPrinter(object):
    def __init__(self):
        pass

    def notify(self, event):
        # TickEvent handler
        print random()