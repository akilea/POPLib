from ursina import *
from ursina import shaders
from enum import Enum
from popgame.game_engine.team_util import *
from popgame.math import length_squared_2D
from popgame.game_engine.game_event_subscription import *

class CombatUnitWatcher(Entity):
    def __init__(self,team_info:ETeamInfo,unit_type:EUnitInfo,cu_subscription:CombatUnitSubscription=CombatUnitSubscription()) -> None:
        super().__init__()
        self._old_position = Vec3()
        self._velocity = Vec3()
        
        self._ghost = Text("Ghost",parent=self,scale=30.0,position=Vec3(0,3,0),color=color.yellow,billboard=True,shader=shaders.unlit_shader,origin=(0.0,0.5))
        self._ghost.visible_setter(False)
        self._ghost.create_background(self._ghost.size*0.5,self._ghost.size*0.8,color.red)
        
        self._team_info = team_info
        self._unit_type = unit_type
        self._hp = self._unit_type.max_hp
        self._one_over_delta = 60.0
        self.cu_subscription = cu_subscription
        self._frame_count = random.randrange(1,VELOCITY_CHECK_MODULE_RANGE-1)

    @property
    def unit_type(self):
        return self._unit_type
    
    @property
    def team_info(self):
        return self._team_info
    
    def get_velocity(self):
        return CombatUnitWatcher.game_space_to_boid_space(self._velocity)
    
    # def get_position(self):
    #     return CombatUnitWatcher.game_space_to_boid_space(self._velocity)
        
    @property
    def damage_multiplier(self):
        return self.unit_type.damage_multiplier
    
    def update(self):
        self._velocity = (self._old_position - self.world_position) * self._one_over_delta
        self._old_position = copy(self.world_position)
        self._frame_count += 1

    def velocity_check(self)->bool:
        ret = False
        if self._frame_count % VELOCITY_CHECK_MODULE_RANGE == 0:
            v = self.get_velocity()
            if length_squared_2D(v) > self.unit_type.max_velocity_squared:
                self.cu_subscription.on_velocity_check_failed_callable(OnVelocityCheckFailed_Payload(v,self.unit_type.max_velocity))
                ret = True
        return ret

    def receive_damage_and_test_death(self,hitpoint:int,projection_direction:Vec2)->bool:
        self._hp -= hitpoint
        self.cu_subscription.on_collision_damage_callable(OnCollisionDamage_Payload(hitpoint,projection_direction))
        return self._hp <= 0
    
    def receive_env_damage_and_test_death(self,hitpoint:int)->bool:
        self._hp -= hitpoint
        return self._hp <= 0
            
    def deal_damage(self,hitpoint:int,projection_direction:Vec2):
        self.cu_subscription.on_deal_damage_callable(OnDealDamage_Payload(hitpoint,projection_direction))
        
    def die(self):
        self._ghost.visible_setter(True)
        self.cu_subscription.on_unit_death_callable(OnUnitDeath_Payload(Vec2(0,0)))
   
    @staticmethod
    def game_space_to_boid_space(position_3D: Vec3) -> Vec2:
        return Vec3(position_3D.z,position_3D.x)