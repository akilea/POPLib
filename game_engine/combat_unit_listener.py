from ursina import *
from enum import Enum
from popgame.game_engine.team_util import *
from popgame.math import length_squared_2D

class CombatUnitListener(Entity):
   
    def __init__(self,team_info:ETeam,unit_type:EUnitType) -> None:
        super().__init__()
        self._old_position = Vec3()
        self._velocity = Vec3()

        self._team_info = team_info
        self._unit_type = unit_type
        self._hp = self._unit_type.max_hp
        self._one_over_delta = 1.0 / 60.0

        self._callable_on_death = lambda *args: None
        self._callable_on_receive_damage = lambda *args: None
        self._callable_on_deal_damage = lambda *args: None
        self._callable_on_velocity_check_fail = lambda *args: None

    @property
    def unit_type(self):
        return self._unit_type
    
    @property
    def team_flag(self):
        return self._team_info
    
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
        return self.unit_type.damage_multiplier
    
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