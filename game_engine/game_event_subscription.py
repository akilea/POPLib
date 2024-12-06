from ursina import *

"""_summary_
Events at the Team level.
    on_build_team: It's time to build your boids, register the team members and register to SpatialHash.
    on_match_start: When the match starts,unpause your boids and systems.
    on_match_stop: When the match stops, pause your boids and systems.
    on_cleanup_team: Unregister team members, destroy boids, unregister from SpatialHash.
    on_unit_death_callable: When of of YOUR team member dies.
    on_team_elimiated: When your team has 0 team member alive.
    on_team_winning: When you are the only team left.
"""
class TeamSubscription:
    def __init__(self) -> None:
        self.on_build_team_callable = lambda payload: None
        self.on_match_start_callable = lambda payload: None
        self.on_match_stop_callable = lambda payload: None
        self.on_cleanup_team_callable = lambda payload: None
        self.on_unit_death_callable = lambda payload: None
        self.on_team_elimiated_callable = lambda payload: None
        self.on_team_winning_callable = lambda payload: None

"""_summary_
Events at the BoidCombatUnit level.
    on_unit_death: When this unit dies.
    on_collision_damage: When this unit receive damage from another boid (collision).
    on_deal_damage: When you deal damage to another boid.
    on_velocity_check_failed: When your boid goes too fast and takes damage.
    on_receive_zone_damage: When your boid is in a forbidden zone and takes damage.
"""
class CombatUnitSubscription:
    def __init__(self) -> None:
        self.on_unit_death_callable = lambda payload: None
        self.on_collision_damage_callable = lambda payload: None
        self.on_deal_damage_callable = lambda payload: None
        self.on_velocity_check_failed_callable = lambda payload: None
        self.on_receive_zone_damage_callable = lambda payload: None

class OnBuildTeam_Payload():
    pass

class OnMatchStart_Payload():
    pass

class OnMatchStop_Payload():
    pass

class OnCleanup_Payload():
    pass

class OnTeamEliminated_Payload():
    pass

class OnTeamWinning_Payload():
    pass

class OnUnitDeath_Payload():
    pass
    
class OnCollisionDamage_Payload():
    def __init__(self,projection,damage) -> None:
        self.projection = projection
        self.damage = damage
    
class OnDealDamage_Payload(OnCollisionDamage_Payload):
    pass

class OnVelocityCheckFailed_Payload():
    def __init__(self,current_velocity,max_velocity) -> None:
        self.current_velocity = current_velocity
        self.max_velocity = max_velocity
               
class OnReceiveZoneDamage_Payload():
    def __init__(self,dot,current_damage) -> None:
        self.current_damage = current_damage
        self.damage_over_time = dot