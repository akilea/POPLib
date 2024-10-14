import abc
from ursina import *

@abs
class IBoidAlgorithm:
    def __init__(self, root: Entity=None, debug_color:bool=None,weight:float=1.0):
        pass

    def compute_desired_speed()-> Vec2:
        pass

    def set_weight(self,weight)->None:
        pass

    def get_weight(self,weight)->float:
        pass