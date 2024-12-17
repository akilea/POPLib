
from ursina import *
from popgame.game_engine.team import Team  
from popgame.game_engine.team_util import ETeamInfo
from popgame.game_engine.combat_unit_watcher import CombatUnitWatcher  
from popgame.game_engine.team_util import *
from popgame.boid_system.spatial_hash import SpatialHash
from popgame.constant import UNIT_DAMAGE_RADIUS_SQUARED
from popgame.boid_system.boid_algorithm_repulse import BoidAlgorithmRepulse
from popgame.game_engine.game_event_subscription import *
from popgame.game_engine.zone import SoftBorderDamageZone,HardBorderDamageZone
from popgame.math import *
from itertools import combinations

class CombatSimulator(Entity):
    def __init__(self,callable_on_bcu_death):
        super().__init__()
        self._team_dict = dict()
        self._total_team_mask = 0x000000
        #Little hacky but good enough
        self._boid_to_combat_unit_watcher_map = dict()
        self._boid_to_repulse_algo_map = dict()
        self._internal_on_bcu_death_callable = callable_on_bcu_death
        
        self._zones = list()
        self._zones.append(SoftBorderDamageZone())
        self._zones.append(HardBorderDamageZone())
        
    @property
    def total_team_mask(self):
        return self._total_team_mask
        
    def build_teams(self):
        for team_info,team in self._team_dict.items():
            team._ge_subscription.on_build_team_callable(OnBuildTeam_Payload())
            #Register all mapped boids to their combat unit
            for cu,unit_info in team._dict_cu_to_unity_type.items() :
                cuw = CombatUnitWatcher(team_info=team_info,unit_type=unit_info,cu_subscription=team._dict_cu_to_sub[cu])
                cuw.parent=cu
                self._boid_to_combat_unit_watcher_map[cu.get_boid()] = cuw
                
                balgo_rep = BoidAlgorithmRepulse()
                self._boid_to_repulse_algo_map[cu.get_boid()] = balgo_rep
                cu.add_algorithm(balgo_rep)
                balgo_rep.set_owner(cu.get_boid())
                
                cu.scale *= unit_info.model_scale

    def update(self):
        if not self.ignore:
            self.produce_pairs()
            self.velocity_check()
            self.zone_check()
        
    def produce_pairs(self):
        sh = SpatialHash.instance()
        for bs in sh._cells.values():
            if len(bs) > 1:
                cell_pairs = list(combinations(bs, 2))
                cell_pairs_en = filter(CombatSimulator.are_ennemy_tuple,cell_pairs)
                cell_pairs_en_alive = filter(CombatSimulator.are_alive,cell_pairs_en)
                for pair in cell_pairs_en_alive:
                    if UNIT_DAMAGE_RADIUS_SQUARED > pair[0].get_squared_distance_from(pair[1].get_position()):
                        self.resolve_damage(pair[0],pair[1])

    def velocity_check(self):
        for boid,bcu_w in self._boid_to_combat_unit_watcher_map.items():
            if bcu_w.is_alive() and bcu_w.velocity_check():
                if bcu_w.receive_env_damage_and_test_death(VELOCITY_CHECK_DAMAGE):
                    self.kill_unit(bcu_w,boid)

    def zone_check(self):
        for zone in self._zones:
            if zone.tick():
                for boid,bcu_w in self._boid_to_combat_unit_watcher_map.items():
                    if bcu_w.is_alive() and zone.is_exterior(boid.get_position()):
                        bcu_w.cu_subscription.on_receive_zone_damage_callable(OnReceiveZoneDamage_Payload(zone.get_damage()))
                        if bcu_w.receive_env_damage_and_test_death(zone.get_damage()):
                            self.kill_unit(bcu_w,boid)
        
    def resolve_damage(self,bA,bB):
        repA = self._boid_to_repulse_algo_map[bA]
        repB = self._boid_to_repulse_algo_map[bB]
        if repA.activated or repA.activated:
            return

        cuwA = self._boid_to_combat_unit_watcher_map[bA]
        cuwB = self._boid_to_combat_unit_watcher_map[bB]
        deltaMomentumBToA = bA.get_velocity() - bB.get_velocity()
        directionBtoA = change_length_2D(bA.get_position() - bB.get_position(),1.0)
        attack_multiplier = dot_2D(directionBtoA,deltaMomentumBToA)
        winner_is_a = attack_multiplier > 0.0
        winner_cuw = cuwA if winner_is_a else cuwB
        loser_cuw = cuwA if not winner_is_a else cuwB
        projectionWinToLost = deltaMomentumBToA if winner_is_a else -deltaMomentumBToA
        projectionWinToLost = change_length_2D(projectionWinToLost)
        attack_dmg = int(abs(attack_multiplier) * winner_cuw.damage_multiplier)

        if attack_dmg < 0:
            raise Exception("Damage negative: impossible!")
        if attack_dmg == 0:
            attack_dmg = 1
            
        winner_boid = bA if winner_is_a else bB
        loser_boid = bA if not winner_is_a else bB

        winner_cuw.deal_damage(attack_dmg,-projectionWinToLost)
        if loser_cuw.receive_damage_and_test_death(attack_dmg,projectionWinToLost):
            self.kill_unit(loser_cuw,loser_boid)
        else:
            rep_algoL = self._boid_to_repulse_algo_map[loser_boid]
            rep_algoL.activate(direction=projectionWinToLost)
            rep_algoW = self._boid_to_repulse_algo_map[winner_boid]
            rep_algoW.activate(direction=-projectionWinToLost)
    
    def match_start(self):
        payload = OnMatchStart_Payload()
        for team in self._team_dict.values():
            team.ge_subscription.on_match_start_callable(payload)
        self.ignore = False

    def match_stop(self):
        payload = OnMatchStop_Payload()
        for team in self._team_dict.values():
            team.ge_subscription.on_match_stop_callable(payload)
        self.ignore = True

    def reset(self):
        payload = OnCleanup_Payload()
        for team in self._team_dict.values():
            team.ge_subscription.on_cleanup_team_callable(payload)

    def kill_unit(self,cuw,boid):
        team_info = cuw.team_info
        payload = OnUnitDeath_Payload(position2D=boid.get_position())
        t = self._team_dict.get(team_info,None)
        if t:
            t.ge_subscription.on_unit_death_callable(payload)

        #Break encapsulation a bit, but better that way
        ba_repulse = self._boid_to_repulse_algo_map.pop(boid, None)
        if ba_repulse is not None:
            ba_repulse.destroy_limb()
        cuw.die()
        boid.set_group_mask(ETeamInfo.Ghost.flag)
        self._internal_on_bcu_death_callable(cuw)
        
    def eliminate_team(self,team_info):
        payload = OnTeamEliminated_Payload()
        t = self._team_dict.get(team_info,None)
        if t:
            t.ge_subscription.on_team_elimiated_callable(payload)

    def win_team(self,team_info):
        payload = OnTeamWinning_Payload()
        t = self._team_dict.get(team_info,None)
        if t:
            t.ge_subscription.on_team_winning_callable(payload)

    def register_team(self,new_team:Team):
        if new_team is None:
            raise Exception("No team provided")
        if new_team in self._team_dict:
            raise Exception("Team already registered")
        if self._total_team_mask & new_team.info.flag != 0:
            raise Exception("Team with flag already registered")
        if not isinstance(new_team,Team):
            raise Exception("Class is not a Team class")
        self._team_dict[new_team.info] = new_team

    @staticmethod
    def are_ennemy_tuple(tuple_b):
        return (tuple_b[0].get_group_mask() & tuple_b[1].get_group_mask()) == 0

    @staticmethod
    def are_ennemy(ba,bb):
        return (ba.get_group_mask() & bb.get_group_mask()) == 0
    
    @staticmethod
    def are_alive(tuple_b):
        return (tuple_b[0].get_group_mask() != 0 and tuple_b[1].get_group_mask()) != 0
    
    @staticmethod
    def are_friend(ba,bb):
        return (ba.get_group_mask() & bb.get_group_mask()) != 0