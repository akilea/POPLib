from ursina.color import Color
from popgame.game_engine.combat_unit_watcher import CombatUnitWatcher
from popgame.game_engine.team_util import ETeamInfo,EUnitInfo,MAX_ALLOWED_POINTS
class Team:
    def __init__(self,team_info):
        self._info = team_info
        if team_info.flag % 2 != 0:
            raise Exception("Team is a flag, not a mask: only a single bit needs to be used.")
        self._dict_cu_to_unity_type = dict()
        
    @property
    def info(self):
        return self._info
    
    def boid_combat_units(self):
        return self._dict_cu_to_unity_type.keys()
        
    """Create Boid Combat Units inside""" 
    def on_build_team(self):
        raise NotImplementedError()

    """Boids can start moving""" 
    def on_start(self):
        raise NotImplementedError()
    
    """Boids must update""" 
    def on_update(self):
        raise NotImplementedError()
    
    """Boids must stop moving""" 
    def on_stop(self):
        raise NotImplementedError()
    
    """Systems must reset as if empty. You will need to customize this."""
    def on_reset(self):
        self._dict_cu_to_unity_type.clear()
    
    def register_boid(self,bcu,unit_type:EUnitInfo):
        if bcu in self._dict_cu_to_unity_type.keys():
            raise Exception("Boid Combat Unit already registered!")
        pt = self.compute_total_point()
        if pt > MAX_ALLOWED_POINTS:
            raise Exception(f"Max amounts of points {MAX_ALLOWED_POINTS} surpassed (is {pt})!")
        
        print (f"Max amounts of points {MAX_ALLOWED_POINTS} surpassed (is {pt})!")
              
        self._dict_cu_to_unity_type[bcu] = unit_type
        
    def compute_total_point(self):
        pt = 0
        for v in self._dict_cu_to_unity_type.values():
            pt += v.cost
        return pt