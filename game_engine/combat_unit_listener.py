from ursina import *
from enum import Enum
from popgame.math import length_squared_2D

class CombatUnitListener(Entity):
    class EUnitType(Enum):
        Light = 1
        Medium = 2
        Heavy = 3

    class EDamageType(Enum):
        Collision = 1
        VelocityLimit = 2
        Zone = 3
    
    def __init__(self,unit_type:EUnitType,team_flag) -> None:
        super().__init__()
        self._old_position = Vec3()
        self._velocity = Vec3()

        self._team_flag = team_flag
        self._unit_type = unit_type
        self._max_hp = -100
        self._hp = self._max_hp
        self._max_velocity = -100
        self._max_velocity_squared = -100
        self._damage_multiplier = 1.0
        self._one_over_delta = 1.0 / 60.0
        match unit_type:
            case CombatUnitListener.EUnitType.Light:
                self._max_hp = 100
                self._max_velocity = 20
                self._damage_multiplier = 1
            case CombatUnitListener.EUnitType.Medium:
                self._max_hp = 200
                self._max_velocity = 15
                self._damage_multiplier = 2
            case CombatUnitListener.EUnitType.Heavy:
                self._max_hp = 350
                self._max_velocity = 10
                self._damage_multiplier = 3
            case _:
                raise Exception("Invalid unit type!")
        self._max_velocity_squared = self._max_velocity * self._max_velocity
        self._hp = self._max_hp

        self._callable_on_death = lambda *args: None
        self._callable_on_receive_damage = lambda *args: None
        self._callable_on_deal_damage = lambda *args: None
        self._callable_on_velocity_check_fail = lambda *args: None

    @property
    def unit_type(self):
        return self._unit_type
    
    @property
    def team_flag(self):
        return self._team_flag
    
    def get_velocity(self):
        return CombatUnitListener.game_space_to_boid_space(self._velocity)
    
    def get_position(self):
        return CombatUnitListener.game_space_to_boid_space(self._velocity)
    
    def subscribe_on_death(self,callable_on_death):
        self._callable_on_death

    def subscribe_on_receive_damage(self,callable_on_death):
        self._callable_on_receive_damage

    def subscribe_on_deal_damage(self,callable_on_death):
        self._callable_on_deal_damage

    def on_velocity_check_fail(self,callable_on_death):
        self._callable_on_velocity_check_fail
        
    @property
    def damage_multiplier(self):
        return self._damage_multiplier
    
    def update(self):
        self._velocity = (self.position - self.position) * self._one_over_delta
        self._current_position = copy(self.position)

    def velocity_check(self):
        v = self.get_velocity()
        if length_squared_2D(v) > self._max_velocity_squared:
            self._callable_on_velocity_check_fail(v)

    def receive_damage_and_test_death(self,hitpoint:int,projection_direction:Vec2)->bool:
        self._hp -= hitpoint
        self._callable_on_receive_damage(hitpoint,projection_direction)
        return self._hp <= 0
            
    def deal_damage(self,hitpoint:int,projection_direction:Vec2):
        self._callable_on_deal_damage(hitpoint,projection_direction)
        
    def die(self):
        self._callable_on_death()
   
    @staticmethod
    def game_space_to_boid_space(position_3D: Vec3) -> Vec2:
        return Vec3(position_3D.z,position_3D.x)