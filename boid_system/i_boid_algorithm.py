from abc import ABC, abstractmethod
from popgame.boid_system.i_restricted_boid import IRestrictedBoid
from ursina import *

class IBoidAlgorithm(ABC):
    def __init__(self,weight:float=1.0):
        pass

    @abstractmethod
    def set_owner(self,owner_boid:IRestrictedBoid)-> None:
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