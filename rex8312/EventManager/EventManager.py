# -*-coding: utf-8 -*-

__author__ = 'rex8312'

from Views import RandomNumberPrinter
from Controllers import CPUSpinner
from Events import TickEvent
from Events import NullEvent


class EventManager(object):
    def __init__(self):
        self.listeners = dict()

    def register_listener(self, listener, event_type, method='notify'):
        if event_type != NullEvent:
            self.listeners.setdefault(event_type, list())
            self.listeners[event_type].append(getattr(listener, method))
        listener.ev_manager = self

    def unregister_listener(self, listener, event_type, method='notify'):
        if event_type in self.listeners:
            self.listeners[event_type].remove(getattr(listener, method))

    def post(self, event):
        event_type = type(event)
        listeners = self.listeners[event_type]
        for listener in listeners:
            listener(event)



if __name__ == '__main__':
    # dict 기반 이벤트 핸들러
    ev_manager = EventManager()

    rnprinter = RandomNumberPrinter()
    cpuspinner = CPUSpinner()

    # rnprinter는 TickEvent를 받으면 notify 메소드를 호출
    ev_manager.register_listener(rnprinter, TickEvent, 'notify')
    # cpuspnner는 event 핸들러가 없음,
    # NullEvent를 전달하면 listener.ev_manager에 이벤트 매니저를 전달하기만 함
    ev_manager.register_listener(cpuspinner, NullEvent)

    cpuspinner.run()

