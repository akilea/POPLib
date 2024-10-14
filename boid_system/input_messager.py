from ursina import *

class InputMessager(Entity):
    def __init__(self):
        super().__init__()
        self._subscribers = []

    def add_subscriber(self,obj):
        if hasattr(obj,"input") or hasattr(obj,"input_hold"):
            self._subscribers.append(obj)
        else:
            raise Exception("Object without input or input_hold method! Add the input or input_hold method to fix this.")

    def remove_subscriber(self,obj):
        if obj in self._subscribers:
            self._subscribers.remove(obj)
        else:
            raise Exception("This object is not subscribed!")

    def input(self,key):
        # print(key)
        for x in self._subscribers:
            if hasattr(x,"input"):
                x.input(key)