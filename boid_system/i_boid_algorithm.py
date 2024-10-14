from abc import ABC, abstractmethod
from ursina import *

class IBoidAlgorithm(ABC):
    def __init__(self, root: Entity=None, debug_color:bool=None,weight:float=1.0):
        pass

    @abstractmethod
    def compute_desired_speed()-> Vec2:
        pass

    @abstractmethod
    def set_weight(self,weight)->None:
        pass

    @abstractmethod
    def get_weight(self,weight)->float:
        pass