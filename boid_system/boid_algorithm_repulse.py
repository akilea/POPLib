from boid_algorithm import BoidAlgorithm
from limb_debug import LimbDebug,LimbDebugNullObject
from popgame.constant import UNIT_REPULSE_TIME,UNIT_REPULSE_VELOCITY
from ursina import *   

class BoidAlgorithmRepulse(BoidAlgorithm):
    def __init__(self, weight = 10000.0,repulsion_time=UNIT_REPULSE_TIME,velocity_magnitude=UNIT_REPULSE_VELOCITY):
        super().__init__( color.brown, weight)
        self._velocity_to_keep = Vec2(1.0,0.0)
        self._velocity_magnitude = velocity_magnitude
        self._repulsion_time = repulsion_time
        self._seq = Sequence(Wait(self._repulsion_time))

    def activate(self,direction=Vec2(1.0,0.0)):
        self._seq.finish()
        self._velocity_to_keep =  direction * self._velocity_magnitude
        self._seq.start()

    @property
    def activated(self):
        return self._seq.started and not self._seq.finished

    def compute_desired_speed(self):
        if self.activated:
            self._update_limb(self._velocity_to_keep)
            return self._velocity_to_keep
        return None
    
    def destroy_limb(self):
        if not isinstance( self._debug_limb,LimbDebugNullObject):
            self._debug_limb._eternal = False
            destroy(self._debug_limb)