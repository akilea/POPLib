from ursina import *
from ursina import Vec2
from popgame.unit_test.scene_creation import  *
from popgame.constant import *
from popgame.game_engine.combat_unit_watcher import Ticker

class ExternalZone(Entity):
    def __init__(self,position:Vec2, size:float,c1,c2,flash_time,dmg):
        super().__init__(True,True)
        size_vec = Vec2(size,size)
        c = create_corners(position-size_vec,position+size_vec,0.1)
        self._min_corner = c[0]
        self._min_corner = Vec2(self._min_corner.x,self._min_corner.z)
        self._max_corner = c[2]
        self._max_corner = Vec2(self._max_corner.x,self._max_corner.z)
        lines = []
        lines.append(create_line(c[0],c[1],c1,width=0.3))
        lines.append(create_line(c[1],c[2],c1,width=0.3))
        lines.append(create_line(c[2],c[3],c1,width=0.3))
        lines.append(create_line(c[3],c[0],c1,width=0.3))
        self._dmg = dmg
        
        for l in lines:
            s = Sequence(
                Func(l.animate_color,c2,flash_time),
                Wait(flash_time),
                Func(l.animate_color,c1,flash_time),
                Wait(flash_time),
                loop=True
            )
            s.start()
            
        self._ticker = Ticker(ZONE_CHECK_MODULE_RANGE,ZONE_CHECK_MODULE_RANGE)
            
    def tick(self):
        return self._ticker.tick()
            
    def is_exterior(self,boid_2D_position):
        return boid_2D_position.x > self._max_corner.x or boid_2D_position.x < self._min_corner.x or boid_2D_position.y > self._max_corner.y or boid_2D_position.y < self._min_corner.y          
        
    def get_damage(self):
        return self._dmg
            
class SoftBorderDamageZone(ExternalZone):
    def __init__(self):
        c1 = color.white50
        c2 = hsv(0, 1, 1,0.5)
        super().__init__(Vec3(0,0,0), SOFT_BORDER_HALF_SIZE, c1, c2,1.0,SOFT_BORDER_ZONE_CHECK_DAMAGE)
        
class HardBorderDamageZone(ExternalZone):
    def __init__(self):
        c1 = color.black50
        c2 = hsv(0, 0, 1,0.5)
        super().__init__(Vec3(0,0,0), WORLD_HALF_SIZE, c1, c2,0.7,HARD_BORDER_ZONE_CHECK_DAMAGE)