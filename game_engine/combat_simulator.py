
from ursina import *
from popgame.game_engine.team import Team  
from popgame.game_engine.combat_unit_listener import CombatUnitListener  
from popgame.game_engine.team_util import TeamUtil
from popgame.boid_system.spatial_hash import SpatialHash
from popgame.constant import UNIT_DAMAGE_RADIUS_SQUARED
from popgame.math import *
from itertools import combinations

class CombatSimulator(Entity):
    def __init__(self,callable_on_bcu_death):
        super().__init__()
        self._team_set = set()
        self._total_team_mask = 0x000000
        #Little hacky but good enough
        self._boid_to_combat_unit_listener_map = dict()
        self._callable_on_bcu_death = callable_on_bcu_death
        
    @property
    def total_team_mask(self):
        return self._total_team_mask
        
    def build_teams(self):
        for team in self._team_set:
            pos = TeamUtil.get_team_position(team.team_flag)
            col = TeamUtil.get_team_color(team.team_flag)
            contr = TeamUtil.get_team_input_control(team.team_flag)
            team.on_build_team(col,pos,contr,TeamUtil.MAX_ALLOWED_SPAWN_SQUARE_HALF_SIZE,TeamUtil.MAX_ALLOWED_POINTS)
            #Register all mapped boids to their combat unit
            for cu in team._combat_unit_set :
                cul = CombatUnitListener(unit_type=CombatUnitListener.EUnitType.Light,team_flag=team.team_flag)
                self._boid_to_combat_unit_listener_map[cu.get_boid()] = cul

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
                cell_pairs_filtered = filter(CombatSimulator.are_ennemy_tuple,cell_pairs)
                for pair in cell_pairs_filtered:
                    if UNIT_DAMAGE_RADIUS_SQUARED > pair[0].get_squared_distance_from(pair[1].get_position()):
                        self.resolve_damage(pair[0],pair[1])

    def resolve_damage(self,bA,bB):
        culA = self._boid_to_combat_unit_listener_map[bA]
        culB = self._boid_to_combat_unit_listener_map[bB]
        deltaMomentumBToA = bA.get_velocity() * culA.unit_type.value - bB.get_velocity() * culB.unit_type.value
        directionBtoA = change_length_2D(bA.get_position() - bB.get_position(),1.0)
        attack_multiplier = dot_2D(directionBtoA,deltaMomentumBToA)
        winner_is_a = attack_multiplier > 0.0
        winner_cu = culA if winner_is_a else culB
        looser_cu = culA if not winner_is_a else culB
        projectionWinToLost = -deltaMomentumBToA if winner_is_a else deltaMomentumBToA
        attack_dmg = int(abs(attack_multiplier) * winner_cu.damage_multiplier)

        if attack_dmg < 0:
            raise Exception("Yikes!")
        if attack_dmg == 0:
            attack_dmg = 1

        winner_cu.deal_damage(attack_dmg,-projectionWinToLost)
        print("OUCH")
        if looser_cu.receive_damage_and_test_death(attack_dmg,projectionWinToLost):
            print("DIE")
            looser_cu.die()
            self._callable_on_bcu_death(looser_cu)

    @staticmethod
    def are_ennemy_tuple(tuple_b):
        return (tuple_b[0].get_group_mask() & tuple_b[1].get_group_mask()) == 0

    @staticmethod
    def are_ennemy(ba,bb):
        return (ba.get_group_mask() & bb.get_group_mask()) == 0
    
    @staticmethod
    def are_friend(ba,bb):
        return (ba.get_group_mask() & bb.get_group_mask()) != 0
    
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