
from ursina import *
from popgame.game_engine.team import Team  
from popgame.game_engine.combat_unit_watcher import CombatUnitWatcher  
from popgame.game_engine.team_util import *
from popgame.boid_system.spatial_hash import SpatialHash
from popgame.constant import UNIT_DAMAGE_RADIUS_SQUARED
from popgame.boid_system.boid_algorithm_repulse import BoidAlgorithmRepulse
from popgame.math import *
from itertools import combinations

class CombatSimulator(Entity):
    def __init__(self,callable_on_bcu_death):
        super().__init__()
        self._team_set = set()
        self._total_team_mask = 0x000000
        #Little hacky but good enough
        self._boid_to_combat_unit_listener_map = dict()
        self._boid_to_repulse_algo_map = dict()
        self._callable_on_bcu_death = callable_on_bcu_death
        
    @property
    def total_team_mask(self):
        return self._total_team_mask
        
    def build_teams(self):
        for team in self._team_set:
            team_info = team._info
            pos = team_info.rel_start_pos
            col = team_info.color
            contr = team_info.control_dict
            team.on_build_team()
            #Register all mapped boids to their combat unit
            for cu,unit_type in team._dict_cu_to_unity_type.items() :
                cuw = CombatUnitWatcher(team_info=team_info,unit_type=unit_type)
                self._boid_to_combat_unit_listener_map[cu.get_boid()] = cuw
                balgo_rep = BoidAlgorithmRepulse()
                self._boid_to_repulse_algo_map[cu.get_boid()] = balgo_rep
                cu.add_algorithm(balgo_rep)
                balgo_rep.set_owner(cu.get_boid())

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
        repA = self._boid_to_repulse_algo_map[bA]
        repB = self._boid_to_repulse_algo_map[bB]
        if repA.activated or repA.activated:
            return

        cuwA = self._boid_to_combat_unit_listener_map[bA]
        cuwB = self._boid_to_combat_unit_listener_map[bB]
        deltaMomentumBToA = bA.get_velocity() * cuwA.unit_type.value - bB.get_velocity() * cuwB.unit_type.value
        directionBtoA = change_length_2D(bA.get_position() - bB.get_position(),1.0)
        attack_multiplier = dot_2D(directionBtoA,deltaMomentumBToA)
        winner_is_a = attack_multiplier > 0.0
        winner_cuw = cuwA if winner_is_a else cuwB
        loser_cuw = cuwA if not winner_is_a else cuwB
        projectionWinToLost = deltaMomentumBToA if winner_is_a else -deltaMomentumBToA
        projectionWinToLost = change_length_2D(projectionWinToLost)
        attack_dmg = int(abs(attack_multiplier) * winner_cuw.damage_multiplier)

        if attack_dmg < 0:
            raise Exception("Yikes!")
        if attack_dmg == 0:
            attack_dmg = 1

        print(attack_dmg)
        winner_cuw.deal_damage(attack_dmg,-projectionWinToLost)
        if loser_cuw.receive_damage_and_test_death(attack_dmg,projectionWinToLost):
            loser_cuw.die()
            self._callable_on_bcu_death(loser_cuw)
        else:
            winner_boid = bA if winner_is_a else bB
            loser_boid = bA if not winner_is_a else bB

            rep_algoL = self._boid_to_repulse_algo_map[loser_boid]
            rep_algoL.activate(direction=projectionWinToLost)
            rep_algoW = self._boid_to_repulse_algo_map[winner_boid]
            rep_algoW.activate(direction=-projectionWinToLost)

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
        if self._total_team_mask & new_team.info.flag != 0:
            raise Exception("Team with flag already registered")
        if not isinstance(new_team,Team):
            raise Exception("Class is not a Team class")
        self._team_set.add(new_team)