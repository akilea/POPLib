from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ..math import length_3D
from .sample_texture import *
from ..boid_system.spatial_hash import *
from ..game_engine.team_util import TeamUtil
from ..constant import *

def run_basic_scene():
    app = Ursina()
    app.border_less = False
    d = DirectionalLight(True)
    d.look_at(Vec3(1,-1,1))
    en = Entity(model='cube', scale=WORLD_SIZE, texture=stone_design1,shader=lit_with_shadows_shader)
    en.set_position(Vec3(0.0,-WORLD_HALF_SIZE,0.0))
    l = Lava()
    sk = Sky(color=color.light_gray)
    cam = EditorCamera(position=Vec3(0,50,-100),rotation=(27,0,0))
    return app

def run_border_scene():
    app = run_basic_scene()
    c = create_corners(SOFT_BORDER_BOUNDARY_MIN,SOFT_BORDER_BOUNDARY_MAX,0.05)
    create_line(c[0],c[1],color.orange)
    create_line(c[1],c[2],color.orange)
    create_line(c[2],c[3],color.orange)
    create_line(c[3],c[0],color.orange)
    return app

def run_border_scene_with_team_zones():
    app = run_border_scene()
    create_team_zones()
    return app

def run_level_grass_scene():
    app = run_border_scene()
    border_right = Entity(model='cube', scale=Vec3(1,WORLD_HEIGHT,WORLD_SIZE), texture=brick_wall,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
    border_right.set_position(Vec3(WORLD_HALF_SIZE,WORLD_HALF_HEIGHT,0))

    border_left = Entity(model='cube', scale=Vec3(1,WORLD_HEIGHT,WORLD_SIZE), texture=brick_wall,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
    border_left.set_position(Vec3(-WORLD_HALF_SIZE,WORLD_HALF_HEIGHT,0))

    border_up = Entity(model='cube', scale=Vec3(WORLD_SIZE,WORLD_HEIGHT,0.0), texture=brick_wall,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
    border_up.set_position(Vec3(0,WORLD_HALF_HEIGHT,WORLD_HALF_SIZE))

    border_dpwn = Entity(model='cube', scale=Vec3(WORLD_SIZE,WORLD_HEIGHT,0.0), texture=brick_wall,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
    border_dpwn.set_position(Vec3(0,WORLD_HALF_HEIGHT,-WORLD_HALF_SIZE))
    return app

def run_generic_test_scene():
    app = run_border_scene()
    f = Text(text='Appuyer sur F pour échouer le test!')
    f.position = Vec3(-1,0.15,0)
    f.origin = Vec2(0,0)
    f.color = color.red
    e = TriggerTestFailureEntity()
    return app

def create_expected_result_text(expect_result : str)->None:
    f = Text(text=expect_result)
    f.color = color.green
    f.position = Vec3(-0.7,0.15,0)


def create_cloudy_castle():
    castle = Entity()
    app = run_border_scene_with_team_zones()
    castle_texture = 'brick'  # You can replace this with your custom texture path

    # Create the castle walls
    wall_thickness = 1
    wall_height = 7
    castle_width = 15
    castle_length = 20

    # Front and back walls
    w1 = create_wall(position=(0, wall_height/2, castle_length/2), scale=(castle_width, wall_height, wall_thickness), texture=castle_texture)
    w1.parent = castle

    w2 = create_wall(position=(0, wall_height/2, -castle_length/2), scale=(castle_width, wall_height, wall_thickness), texture=castle_texture)
    w2.parent = castle

    # Side walls
    w3 = create_wall(position=(castle_width/2, wall_height/2, 0), scale=(wall_thickness, wall_height, castle_length), texture=castle_texture)
    w3.parent = castle
    w4 = create_wall(position=(-castle_width/2, wall_height/2, 0), scale=(wall_thickness, wall_height, castle_length), texture=castle_texture)
    w4.parent = castle

    # Castle gate
    gate = Entity(model='cube', position=(0, wall_height/4, castle_length/2 - 0.5), scale=(5, wall_height/2, wall_thickness), texture='wood', color=color.brown)
    gate.parent = castle
    # Create towers
    tower_height = 10
    tower_radius = 2

    tower1 = Entity(model='cylinder', position=(-castle_width/2, tower_height/2, castle_length/2), scale=(tower_radius, tower_height, tower_radius), texture=castle_texture, collider='box')
    tower1.parent = castle
    tower2 = Entity(model='cylinder', position=(castle_width/2, tower_height/2, castle_length/2), scale=(tower_radius, tower_height, tower_radius), texture=castle_texture, collider='box')
    tower2.parent = castle
    tower3 = Entity(model='cylinder', position=(-castle_width/2, tower_height/2, -castle_length/2), scale=(tower_radius, tower_height, tower_radius), texture=castle_texture, collider='box')
    tower3.parent = castle
    tower4 = Entity(model='cylinder', position=(castle_width/2, tower_height/2, -castle_length/2), scale=(tower_radius, tower_height, tower_radius), texture=castle_texture, collider='box')
    tower4.parent = castle
    castle.rotation = Vec3(0,180,0)
    castle.position = Vec3(0,0,WORLD_HALF_SIZE+10)

    # Create some clouds
    cloud1 = Cloud(position=(-20, 15, -10), scale=(6, 3, 3), speed=0.02)
    cloud2 = Cloud(position=(0, 18, -15), scale=(7, 4, 4), speed=0.015)
    cloud3 = Cloud(position=(20, 12, 5), scale=(6, 2, 2), speed=0.01)
    cloud3 = Cloud(position=(-10, 9, 10), scale=(3, 1, 1), speed=0.03)

    # Add a radiant sun
    sun = Entity(model='sphere', position=(30, 10, -10), scale=(5, 5, 5), texture='white_cube', color=color.yellow)

    # Add a light to make the sun radiant
    sun_light = PointLight(parent=sun, position=(0, 0, 0), color=color.yellow, radius=50, intensity=1.5)

    return app

#########################
#Scene creation helpers
#########################
def create_line(start,finish,color,width=0.1):
    delta = finish-start
    length = length_3D(delta)
    center = (finish+start)*0.5
    l = Entity(model='plane', scale=Vec3(width,width,length),color=color)
    l.set_position(center)
    l.look_at(center+delta)
    return l

class TriggerTestFailureEntity(Entity):
    def input(self,key):
        if key == "f":
            assert(False)

class Cloud(Entity):
    def __init__(self, position=(0, 0, 0), scale=(5, 2, 2), speed=0.01):
        super().__init__(
            model='cube',
            texture='white_cube',  # You can replace this with a cloud texture
            color=color.white,
            position=position,
            scale=scale,
            collider=None
        )
        self.speed = speed
        self.rotation_x=19.0

    def update(self):
        self.x += self.speed  # Move the cloud slowly to the right
        if self.x > 50:  # Reset position if it goes too far
            self.x = -50

def create_wall(position, scale, texture):
    return Entity(model='cube', position=position, scale=scale, texture=texture, collider='box')

class Lava(Entity):
    def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        self.lower_ground = Entity(model='cube', scale=Vec3(LOWER_GROUND_SIZE,1,LOWER_GROUND_SIZE), texture=lava,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
        self.lower_ground.set_position(Vec3(0,-5,0))
        self.lower_ground.parent = self.parent

    def update(self):
        self.lower_ground.texture_offset += Vec2(0.001,0.0003)

def create_corners(min,max,heigth=0.0):
    a = Vec3(min.x,heigth,min.y)
    b = Vec3(min.x,heigth,max.y)
    c = Vec3(max.x,heigth,max.y)
    d = Vec3(max.x,heigth,min.y)
    return (a,b,c,d)

def create_spatial_hash_debug(debug_grid=True,debug_count=True):
    spatial_hash_entity = create_spatial_hash_grid_model(SPATIAL_HASH_GRID_SIZE,WORLD_SIZE_INT,WORLD_SIZE_INT) if debug_grid else None
    g_count = SpatialHashGridCounter() if debug_count else None
    return (spatial_hash_entity,g_count)

def create_spatial_hash_grid_model(grid_size, width, height):
    """Draw grid lines for each cell in the grid."""
    parent = Entity()
    # Vertical lines
    for x in range(0, width + grid_size, grid_size):
        e = Entity(model=Mesh(vertices=[Vec3(x, 0, 0), Vec3(x, 0, height)], mode='line'), color=color.gray)
        e.parent = parent

    # Horizontal lines
    for y in range(0, height + grid_size, grid_size):
        e = Entity(model=Mesh(vertices=[Vec3(0, 0, y), Vec3(width, 0, y)], mode='line'), color=color.gray)
        e.parent = parent
    parent.set_position(SPATIAL_HASH_VEC_OFFSET)
    return parent



class SpatialHashGridCounter(Entity):
    def __init__(self, **kwargs):
        super().__init__(True, True, **kwargs)
        self._text_entity_dict = self.create_spatial_hash_count_model_dict(SPATIAL_HASH_GRID_SIZE,WORLD_SIZE_INT,WORLD_SIZE_INT)
        self._start_index = 0

    def create_spatial_hash_count_model_dict(self,grid_size, width, height):
        """Initialize a dictionary with Text entities for each cell."""
        text_entities = {}
        
        for x in range(int(SPATIAL_HASH_VEC_OFFSET_2D.x), int(SPATIAL_HASH_VEC_OFFSET_2D.x + width), grid_size):
            for y in range(int(SPATIAL_HASH_VEC_OFFSET_2D.y), int(SPATIAL_HASH_VEC_OFFSET_2D.y + height), grid_size):
                cell = SpatialHash.instance().hash(Vec2(x,y))
                center_x = x - grid_size / 2
                center_y = y - grid_size / 2
                parent_entity = Entity(position=Vec3(center_x, SPATIAL_HASH_TEXT_HEIGHT,center_y))
                text_entity = Text(text="0",parent=parent_entity,color=color.black, scale=SPATIAL_HASH_TEXT_SCALE)
                text_entities[cell] = text_entity
        return text_entities

    def update(self):
        self.update_boid_count_texts_deferred(self._text_entity_dict)

    def update_boid_count_texts_deferred(self, text_entities, batch_size=20):
        """Deferred update of boid counts in text entities, batch by batch."""
        cells = list(text_entities.keys())
        total_cells = len(cells)
        
        start_index = self._start_index
        end_index = min(start_index + batch_size, total_cells)
        
        for i in range(start_index, end_index):
            cell = cells[i]
            boid_count = SpatialHash.instance().get_boid_count_in_cell(cell)
            text_entities[cell].text = str(boid_count)

        # Update the start index for the next frame
        self._start_index = end_index if end_index < total_cells else 0

class SpatialHashUnitCounter(Entity):
    def __init__(self, entity_to_attach_to,restricted_boid, distance=30.0,target_mask = 0xFFFFFFF,**kwargs):
        super().__init__(True, True, **kwargs)
        self._text_entity = Text(text="0",parent=self,color=color.black, scale=SPATIAL_HASH_TEXT_BOID_SCALE,position=Vec3(0,6,0),billboard=True)
        self._target_mask = 0xFFFFFFFF
        self._distance = distance
        self._restricted_boid = restricted_boid
        self.parent = entity_to_attach_to
        hash_dist = SpatialHash.instance().safe_hash_range(distance)
        self._str_distance = str("\ndist:") + str(distance) + str("\ncell dist:") + str(hash_dist)

    def update(self):
        nearby_boids = SpatialHash.instance().get_nearby_boids_by_bitmask(self._restricted_boid, self._target_mask,self._distance)
        self._text_entity.text = str(len(nearby_boids)) + self._str_distance
        
class Radius(Entity):
     def __init__(self, entity_to_attach_to, distance=30.0,**kwargs):
        super().__init__(True, True, model=Circle(radius=distance, mode='line', thickness=3),**kwargs)
        self.rotation = Vec3(90,0,0)
        self._text_entity = Text(text="r="+str(distance),parent=entity_to_attach_to,color=color.black, scale=SPATIAL_HASH_TEXT_BOID_SCALE,position=Vec3(0,8,0),billboard=True)
        self.parent = entity_to_attach_to
        
class TeamZone():
    def __init__(self, position:Vec2, size:float, color:Color,name:str):
        cube_col = copy(color)
        cube_col[3] = 0.7
        offset = 0.5
        self._center = Entity(model='quad',color=cube_col,scale=offset,shader=lit_with_shadows_shader)
        self._center.position = Vec3(position.x,offset,position.y)
        size_vec = Vec2(size,size)
        c = create_corners(position-size_vec,position+size_vec,0.05)
        create_line(c[0],c[1],color)
        create_line(c[1],c[2],color)
        create_line(c[2],c[3],color)
        create_line(c[3],c[0],color)
        self._team_text = Text(text=name,parent=self._center,scale=TEAM_ZONE_TEXT_SCALE)
        self._team_text.position = Vec3(0,0.15,0)
        self._team_text.origin = Vec2(0,0)
        self._team_text.color = color
        
def create_team_zones():
    for t in TeamUtil.ETeam:
        if TeamUtil.contains_only_player(t):
            v = t
            p = TeamUtil.get_team_position(v)
            s = TeamUtil.MAX_ALLOWED_SPAWN_SQUARE_HALF_SIZE
            c = TeamUtil.get_team_color(v)
            n = TeamUtil.get_team_name(v)
            TeamZone(p,s,c,n)