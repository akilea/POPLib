from abc import ABC, abstractmethod
from ursina import *

class IRestrictedBoid(ABC):
    @abstractmethod
    def get_position(self)->Vec2:
        pass

    @abstractmethod
    def get_velocity(self)->Vec2:
        pass

    @abstractmethod
    def get_max_velocity(self)->float:
        pass

    @abstractmethod
    def get_distance_from(self,boid_position:Vec2)->float:
        pass

    @abstractmethod
    def get_unit_direction_to(self,boid_position:Vec2)->Vec2:
        pass

    @abstractmethod
    def get_unit_direction_and_distance_to(self,boid_position:Vec2)-> tuple[Vec2,float]:
        pass