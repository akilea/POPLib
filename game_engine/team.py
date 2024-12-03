from ursina.color import Color
from popgame.game_engine.combat_unit_listener import CombatUnitListener
from popgame.game_engine.team_util import ETeam,EUnitType
class Team:
    def __init__(self,team_info):
        self._info = team_info
        if team_info.flag % 2 != 0:
            raise Exception("Team is a flag, not a mask: only a single bit needs to be used.")
        self._dict_cu_to_unity_type = dict()
        
    @property
    def team_flag(self):
        return self._info
    
    def boid_combat_units(self):
        return self._dict_cu_to_unity_type.keys()
        
    """Create Boid Combat Units inside""" 
    def on_build_team(self,team_color:Color,team_position:ETeam,team_control:str, team_radius:float, max_points:int):
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
    
    def register_boid(self,bcu,unit_type:EUnitType):
        if bcu in self._dict_cu_to_unity_type.keys():
            raise Exception("Boid Combat Unit already registered!")
              
        self._dict_cu_to_unity_type[bcu] = unit_type
        
    def compute_total_point(self):
        pt = 0
        for v in self._dict_cu_to_unity_type.values():
            pt += v.value
        return pt