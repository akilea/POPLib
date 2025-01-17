from ursina import Vec2, Vec3

WORLD_SIZE_INT = 100
WORLD_SIZE = float(100.0)
WORLD_HEIGHT = 3.0
WORLD_HALF_HEIGHT = WORLD_HEIGHT*0.5
WORLD_HALF_SIZE = WORLD_SIZE*0.5
WORLD_SIZE_BOUNDARY_MAX = Vec2(WORLD_HALF_SIZE,WORLD_HALF_SIZE)
WORLD_SIZE_BOUNDARY_MIN = -WORLD_SIZE_BOUNDARY_MAX

SOFT_BORDER_SIZE = WORLD_SIZE * 0.8
SOFT_BORDER_HALF_SIZE = SOFT_BORDER_SIZE*0.5
SOFT_BORDER_BOUNDARY_MAX = Vec2(SOFT_BORDER_HALF_SIZE,SOFT_BORDER_HALF_SIZE)
SOFT_BORDER_BOUNDARY_MIN = -SOFT_BORDER_BOUNDARY_MAX

HARD_BORDER_SIZE = WORLD_SIZE
HARD_BORDER_HALF_SIZE = HARD_BORDER_SIZE*0.5
HARD_BORDER_BOUNDARY_MAX = Vec2(HARD_BORDER_HALF_SIZE,HARD_BORDER_HALF_SIZE)
HARD_BORDER_BOUNDARY_MIN = -HARD_BORDER_BOUNDARY_MAX

VELOCITY_MIN = 0.0
VELOCITY_MAX = 20.0

LOWER_GROUND_SIZE = WORLD_SIZE*2.0

SPATIAL_HASH_GRID_HEIGHT = 5.0
SPATIAL_HASH_TEXT_SCALE = 50.0
SPATIAL_HASH_TEXT_BOID_SCALE = 40.0
SPATIAL_HASH_TEXT_HEIGHT = 2.0
SPATIAL_HASH_VEC_OFFSET = Vec3(-WORLD_SIZE*0.5,0.0,-WORLD_SIZE*0.5)
SPATIAL_HASH_VEC_OFFSET_2D = Vec2(-WORLD_HALF_SIZE,-WORLD_HALF_SIZE)

SPATIAL_HASH_GRID_SIZE = 8
SPATIAL_HASH_MAX_DISTANCE_REQUEST = 5

UNIT_DAMAGE_RADIUS = 1.0
UNIT_DAMAGE_RADIUS_SQUARED = UNIT_DAMAGE_RADIUS * UNIT_DAMAGE_RADIUS
UNIT_REPULSE_TIME = 0.5
UNIT_REPULSE_VELOCITY = 19.0

COUNT_DOWN_WAIT_TIME = 0.3

TEAM_ZONE_TEXT_SCALE = 100.0