from ursina import *
from typing import Callable

class InputMessager(Entity):
    def __init__(self):
        super().__init__()
        self._subscribers = set()
        self._input_help = set()

    def add_subscriber(self,callable):
        self._subscribers.add(callable)

    def remove_subscriber(self,callable):
        if callable in self._subscribers:
            self._subscribers.remove(callable)
        else:
            raise Exception("This callable is not subscribed!")

    def input(self,key):
        if InputMessager._is_up_event(key):
            pk = InputMessager._purify_event(key)
            if pk in self._input_help:
                self._input_help.remove(pk)
        else:
            if key not in self._input_help:
                self._input_help.add(key)
    
    @staticmethod
    def _is_up_event(key):
        return key.endswith(" up")
    
    @staticmethod
    def _purify_event(key):
        return key.split(" up", 1)[0]

    def update(self):
        for s in self._subscribers:
            for k in self._input_help:
                s(k)
