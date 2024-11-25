from ursina.color import Color
from popgame.game_engine.team_util import TeamUtil
class Team:
    def __init__(self,team_flag):
        self._team_flag = team_flag
        if team_flag % 2 is not 0:
            raise Exception("Team is a flag, not a mask: only a single bit needs to be used.")
        self._boid_combat_unit_set = set()
        
    @property
    def team_flag(self):
        return self._team_flag
        
    """Create Boid Combat Units inside""" 
    def on_build_team(self,team_color:Color,team_position:TeamUtil.ETeam,team_control:str, team_radius:float, max_points:int):
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
        self._boid_combat_unit_set.clear()
    
    def register_boid(self,bcu):
        if bcu in self._boid_combat_unit_set:
            raise Exception("Boid Combat Unit already registered!")
              
        self._boid_combat_unit_set.add(bcu)