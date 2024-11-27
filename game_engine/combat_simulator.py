
from ursina import *
from popgame.game_engine.team import Team  
from popgame.game_engine.team_util import TeamUtil
from popgame.boid_system.spatial_hash import SpatialHash
from popgame.constant import UNIT_DAMAGE_RADIUS_SQUARED
from itertools import combinations

class CombatSimulator(Entity):
    def __init__(self):
        super().__init__()
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
        self.produce_pairs()
        
    def produce_pairs(self):
        sh = SpatialHash.instance()
        for key,bs in sh._cells.items():
            if len(bs) > 1:
                cell_pairs = list(combinations(bs, 2))
                cell_pairs_filtered = filter(CombatSimulator.are_ennemy_,cell_pairs)
                for pair in cell_pairs_filtered:
                    self.evaluate_damage(pair[0],pair[1])

    @staticmethod
    def are_ennemy_(tuple_b):
        return (tuple_b[0].get_group_mask() & tuple_b[1].get_group_mask()) == 0

    @staticmethod
    def are_ennemy(ba,bb):
        return (ba.get_group_mask() & bb.get_group_mask()) == 0
    
    @staticmethod
    def are_friend(ba,bb):
        return (ba.get_group_mask() & bb.get_group_mask()) != 0
    
    def evaluate_damage(self, bA, bB):
        if UNIT_DAMAGE_RADIUS_SQUARED > bA.get_squared_distance_from(bA.get_position()):
            print("check for instances!",bA,bB)
    
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