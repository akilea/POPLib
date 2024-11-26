
from ursina import *
from popgame.game_engine.team import Team  
from popgame.game_engine.team_util import TeamUtil

class CombatSimulator(Entity):
    def __init__(self):
        self._team_set = set()
        self._total_team_mask = 0x000000
        
    @property
    def total_team_mask(self):
        return self._total_team_mask
        
    def build_teams(self):
        for team in self._team_set:
            pos = TeamUtil.get_team_position(team.team_flag)
            col = TeamUtil.get_team_color(team.team_flag)
            contr = TeamUtil.get_team_input_control(team.team_flag)
            team.on_build_team(col,pos,contr,TeamUtil.MAX_ALLOWED_SPAWN_SQUARE_HALF_SIZE,TeamUtil.MAX_ALLOWED_POINTS)

    def start(self):
        for team in self._team_set:
            team.on_start()

    def update(self):
        for team in self._team_set:
            team.on_update()
        self.evaluate_damage()
        
    def produce_pairs(self):
        #Avec spatial hash, vérifier les paires et les distances. Attention aux limites, on doit faire un test de +1 ou -1
        pass
    
    def evaluate_damage(self, bcuA, bcuB):
        pass
    
    def stop(self):
        for team in self._team_set:
            team.on_stop()

    def reset(self):
        for team in self._team_set:
            team.on_reset()

    def register_team(self,new_team:Team):
        if new_team is None:
            raise Exception("No team provided")
        if new_team in self._team_set:
            raise Exception("Team already registered")
        if self._total_team_mask & new_team.team_flag.value != 0:
            raise Exception("Team with flag already registered")
        if not isinstance(new_team,Team):
            raise Exception("Class is not a Team class")

        self._team_set.add(new_team)