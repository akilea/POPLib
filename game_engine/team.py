from ursina.color import Color
from popgame.game_engine.combat_unit_watcher import CombatUnitWatcher
from popgame.game_engine.game_event_subscription import *
from popgame.game_engine.team_util import ETeamInfo,EUnitInfo,MAX_ALLOWED_POINTS
class Team:
    def __init__(self,team_info:ETeamInfo,ge_subscription:TeamSubscription):
        self._info = team_info
        if team_info.flag % 2 != 0:
            raise Exception("Team is a flag, not a mask: only a single bit needs to be used.")
        self._dict_cu_to_unity_type = dict()
        self._ge_subscription = ge_subscription
        
    @property
    def info(self):
        return self._info
    
    @property
    def ge_subscription(self):
        return self._ge_subscription
    @property
    def boid_combat_units(self):
        return self._dict_cu_to_unity_type.keys()
    
    def unit_info(self,bcu):
        return self._dict_cu_to_unity_type.get(bcu,None)
           
    def reset(self):
        self._dict_cu_to_unity_type.clear()
    
    def register_boid(self,bcu,unit_type:EUnitInfo):
        if bcu in self._dict_cu_to_unity_type.keys():
            raise Exception("Boid Combat Unit already registered!")
        pt = self.compute_total_point()
        if pt > MAX_ALLOWED_POINTS:
            raise Exception(f"Max amounts of points {MAX_ALLOWED_POINTS} surpassed (is {pt})!")
        
        self._dict_cu_to_unity_type[bcu] = unit_type
        
    def compute_total_point(self):
        pt = 0
        for v in self._dict_cu_to_unity_type.values():
            pt += v.cost
        return pt