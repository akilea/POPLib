from ursina import Vec2,Vec3,rotate_around_point_2d,random
from popgame.boid_system import *
import math
from popgame.boid_system.spatial_hash import SpatialHash

#Unsafe (types)
def dot_2D(v1:Vec2,v2:Vec2)->float:
    return v1.x*v2.x+v1.y*v2.y

def dot_3D(v1:Vec2,v2:Vec2)->float:
    return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z

def length_2D(v:Vec2)->float:
    return math.sqrt(v.x*v.x+v.y*v.y)

def length_squared_2D(v:Vec2)->float:
    return v.x*v.x+v.y*v.y

def length_3D(v:Vec3)->float:
    return math.sqrt(v.x*v.x+v.y*v.y+v.z*v.z)

def change_length_2D(v:Vec2,length:float=1.0)->Vec2:
    ret = Vec2(0.0,0.0)
    l = length_2D(v)
    if l > 0.0:
        ret = v*length/length_2D(v)
    return ret

def rotate_2D(v:Vec2,angle_degree:float)->Vec2:
    t = rotate_around_point_2d(v,Vec2(0,0),angle_degree)
    return Vec2(t[0],t[1])

def parameter_constant(value):
    def const(distance):
        return value
    return const

def parameter_inverse(scale, offset):
    def inverse(distance):
        return scale/(distance + offset)
    return inverse

def parameter_squared_inverse(scale, offset):
    def squared_inverse(distance):
        return scale/( distance*distance + offset)
    return squared_inverse
    
def parameter_distance(scale):
    def distance(distance):
        return scale*distance
    return distance

separation_func= parameter_squared_inverse(-25.0,0.1)
#cohesion_func= parameter_inverse(100.0,2.0) #Pas si mal non plus
cohesion_func= parameter_constant(5.0)
separation_funky_func = parameter_squared_inverse(190.0,10.0)

def randomize_boid_position(boid,box_min:Vec2=Vec2(-25.0,-25.0),box_max:Vec2=Vec2(25.0,25.0))->None:
    boid._position.x = random.uniform(box_min.x,box_max.x)
    boid._position.y = random.uniform(box_min.y,box_max.y)
    SpatialHash.instance().update_boid_cell(boid)

def randomize_boid_velocity(boid,vel_min:Vec2=Vec2(-10.0,-10.0),vel_max:Vec2=Vec2(10.0,10.0))->None:
    boid._velocity.x = random.uniform(vel_min.x,vel_max.x)
    boid._velocity.y = random.uniform(vel_min.y,vel_max.y)

def randomize_boid_max_velocity(boid,vel_min:float=5,vel_max:float=20)->None:
    boid._max_velocity = random.uniform(vel_min,vel_max)

def randomize_boid(boid,box_min:Vec2=Vec2(-25.0,-25.0),box_max:Vec2=Vec2(25.0,25.0),vel_min:float=5,vel_max:float=20):
    randomize_boid_position(boid,box_min,box_max)
    randomize_boid_max_velocity(boid,vel_min,vel_max)
    v = Vec2(boid._max_velocity,boid._max_velocity)
    randomize_boid_velocity(boid,-v,v)