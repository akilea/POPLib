from popgame.game_engine.combat_simulator import CombatSimulator
from popgame.game_engine.score_board import ScoreBoard
from ursina import *

class PopEngine(Entity):
    def __init__(self) -> None:
        super().__init__(True,True)
        self._cs = CombatSimulator()
        self._sb = ScoreBoard()
        self._state = 0
        
    def go_to_preparation(self):
        self._sb.display_intro()
        self._cs.build_teams()
        for t in self._cs._team_set:
            self._sb.add_health_bar(t.team_flag)
        self._state = 0

    def go_to_simulation(self):
        self._cs.start()
        self._sb.display_score()

    def go_to_end_game(self):
        self._cs.end()
        self._sb.display_end()

    def input(self,key):
        print(key)
        if "space" == key:
            if self._state == 0:
                self.go_to_simulation()

    
    def update(self):
        pass
    
    def on_bcu_death(self,bcu):
        #ParticleSystem boom!
        #Scoreboard
        pass