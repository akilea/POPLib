from ursina import *
from enum import Enum

class Unit(Entity):
    class EUnitType(Enum):
        Light = 1
        Medium = 2
        Heavy = 3
    
    def __init__(self,unit_type:EUnitType,bcu) -> None:
        self.__bcu = bcu
        self.__unit_type = unit_type
        self.__hp = -100
        self.__max_velocity = -100
        self.__max_velocity_squared = -100
        match unit_type:
            case Unit.EUnitType.Light:
                self.__hp = 100
                self.__max_velocity = 20
            case Unit.EUnitType.Medium:
                self.__hp = 200
                self.__max_velocity = 10
            case Unit.EUnitType.Heavy:
                self.__hp = 500
                self.__max_velocity = 5
            case _:
                raise Exception("Invalid unit type!")
        self.__max_velocity_squared = self.__max_velocity * self.__max_velocity
        
    def speed_check(self):
        pass

    def receive_damage(self,hitpoint:int)->bool:
        self.__hp -= hitpoint
        return self.__hp <= 0
            
    def deal_damage(self,hitpoint:int):
        pass