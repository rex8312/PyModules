__author__ = 'rex8312'

from time import sleep
from Events import TickEvent


class CPUSpinner(object):
    def __init__(self):
        self.ev_manager = None

    def run(self):
        while True:
            sleep(1)
            self.ev_manager.post(TickEvent())