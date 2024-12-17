
from collections import defaultdict
from ursina import *
from ..singleton import *
from ..constant import *

class Cell:
    def __init__(self) -> None:
        self._resident = list()
@Singleton
class SpatialHash(Entity):
    def __init__(self):
        super().__init__()
        self.grid_size = SPATIAL_HASH_GRID_SIZE
        self.half_grid_size = self.grid_size * 0.5
        # Each cell now maps to a list of boids, as groups will be filtered using bitmask
        self._cells = defaultdict(list)
        self._registered_boid_set = set()

    def hash(self, vec):
        """Generate a hash for a position based on grid size."""
        h = (vec.X // self.grid_size, vec.Y // self.grid_size)
        #print(vec,h)
        return h
    
    def hash1D(self,x:float):
        return int(x) // self.grid_size
    
    def safe_hash_range(self,distance:float):
        return self.hash1D(distance)+1

    def register_boid(self, restricted_boid):
        """Add a boid to the grid based on its position."""
        if(restricted_boid in self._registered_boid_set):
            raise Exception("Boid exists already in space hash")
            return
        if(restricted_boid is None):
            raise Exception("Boid added is None")
            return
        cell = self.hash(restricted_boid._position)
        self._cells[cell].append(restricted_boid)
        self._registered_boid_set.add(restricted_boid)

    def unregister_boid(self,restricted_boid):
        cell = self.hash(restricted_boid._position)
        self._cells[cell].remove(restricted_boid)
        self._registered_boid_set.remove(restricted_boid)

    def update_boid_cell(self,restricted_boid):
        """Move a boid from one cell to another if its position changed."""
        if restricted_boid not in self._registered_boid_set:
            return
        old_cell = self.hash(restricted_boid.get_old_position())
        new_cell = self.hash(restricted_boid.get_position())
        # print(f"restricted_boid.get_old_position():{restricted_boid.get_old_position()}, restricted_boid.get_position():{restricted_boid.get_position()}")
        # print(f"old_cell:{old_cell}, new_cell:{new_cell}")
        if old_cell[0] != new_cell[0] or old_cell[1] != new_cell[1]:
            self._cells[old_cell].remove(restricted_boid)
            self._cells[new_cell].append(restricted_boid)

    def remove_boid(self, boid):
        """Remove a boid from its cell when deleted or moved."""
        cell = self.hash(boid._position)
        self._cells[cell].remove(boid)

    def debug_get_all_boids(self,boid, target_mask=0xFFFFFFF,distance=1,include_caller_boid = False):
        raise Exception("Cannot use this method anymore. Use get_nearby_boids_by_bitmask")
        c = copy(self._registered_boid_set)
        if not include_caller_boid:
            try:
                c.remove(boid)
            except ValueError:
                pass
        return c

    def get_nearby_boids_by_bitmask(self, boid, target_mask=0xFFFFFFF,distance=10.0,include_caller_boid = False):
        """Get boids from specific groups (using bitmask) in the neighboring cells."""
        cell_dist = self.safe_hash_range(distance)
        if cell_dist > SPATIAL_HASH_MAX_DISTANCE_REQUEST:
            raise ValueError("Request distance too high.")
        if boid.get_group_mask() == 0:
            return []
        cell_x, cell_y = self.hash(boid._position)
        neighbors = []
        for dx in range(-cell_dist, cell_dist):
            for dy in range(-cell_dist, cell_dist):
                cell = (cell_x + dx, cell_y + dy)
                if cell in self._cells:
                    # Filter boids in this cell using the bitmask
                    neighbors.extend(
                        [other_boid for other_boid in self._cells[cell] 
                         if other_boid.get_group_mask() & target_mask]
                    )
        if not include_caller_boid:
            try:
                neighbors.remove(boid)
            except ValueError:
                pass
        return neighbors
    
    def get_boid_count_in_cell(self, cell):
        """Return the total number of boids in a cell."""
        return len(self._cells[cell])