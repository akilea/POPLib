from combat_simulator import CombatSimulator
from score_board import ScoreBoard
from ursina import *

class PopEngine(Entity):
    def __init__(self) -> None:
        self.__cs = CombatSimulator()
        self.__sb = ScoreBoard()
        self.go_to_preparation()
        #create intro
        #create scores
        #create outro
        
    def go_to_preparation(self):
        self.__cs.build_teams()

    def go_to_simulation(self):
        self.__cs.start()

    def go_to_end_game(self):
        self.__cs.end()
        
    def input(self,key):
        pass
    
    def update(self):
        pass
    
    def on_bcu_death(self,bcu):
        #ParticleSystem boom!
        #Scoreboard
        pass