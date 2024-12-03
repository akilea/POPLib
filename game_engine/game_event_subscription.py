from ursina import *

class TeamSubscription:
    def __init__(self) -> None:
        self.on_game_start = lambda payload: None
        self.on_game_stop = lambda payload: None
        self.on_game_reset = lambda payload: None
        self.on_unit_death_callable = lambda payload: None
        self.on_team_elimiated = lambda payload: None
        self.on_team_winning = lambda payload: None

class CombatUnitSubscription:
    def __init__(self) -> None:
        self.on_unit_death_callable = lambda payload: None
        self.on_collision_damage_callable = lambda payload: None
        self.on_deal_damage_callable = lambda payload: None
        self.on_velocity_check_failed_callable = lambda payload: None
        self.on_receive_zone_damage_callable = lambda payload: None

class OnGameStart_Payload():
    pass

class OnGameStop_Payload():
    pass

class OnGameReset_Payload():
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