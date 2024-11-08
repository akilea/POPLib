
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
        # Each cell now maps to a list of boids, as groups will be filtered using bitmask
        self._cells = defaultdict(list)
        self._registered_boid_set = set()

    def _hash(self, vec):
        """Generate a hash for a position based on grid size."""
        h = (int(vec.x // self.grid_size), int(vec.y // self.grid_size))
        #print(vec,h)
        return h

    def register_boid(self, restricted_boid):
        """Add a boid to the grid based on its position."""
        if(restricted_boid in self._registered_boid_set):
            raise Exception("Boid exists already in space hash")
            return
        if(restricted_boid is None):
            raise Exception("Boid added is None")
            return
        cell = self._hash(restricted_boid._position)
        self._cells[cell].append(restricted_boid)
        self._registered_boid_set.add(restricted_boid)

    def unregister_boid(self,restricted_boid):
        raise NotImplemented()

    def update_boid_cell(self,restricted_boid):
        """Move a boid from one cell to another if its position changed."""
        old_cell = self._hash(restricted_boid.get_old_position())
        new_cell = self._hash(restricted_boid.get_position())
        # print(f"restricted_boid.get_old_position():{restricted_boid.get_old_position()}, restricted_boid.get_position():{restricted_boid.get_position()}")
        # print(f"old_cell:{old_cell}, new_cell:{new_cell}")
        if old_cell[0] != new_cell[0] or old_cell[1] != new_cell[1]:
            self._cells[old_cell].remove(restricted_boid)
            self._cells[new_cell].append(restricted_boid)


    def remove_boid(self, boid):
        """Remove a boid from its cell when deleted or moved."""
        cell = self._hash(boid._position)
        self._cells[cell].remove(boid)

    def get_nearby_boids_by_bitmask(self, boid, target_mask,distance=1):
        """Get boids from specific groups (using bitmask) in the neighboring cells."""
        if distance > SPATIAL_HASH_MAX_DISTANCE_REQUEST:
            raise ValueError("Request distance too high.")
        cell_x, cell_y = self._hash(boid._position)
        neighbors = []
        for dx in [-distance, 0, distance]:
            for dy in [-distance, 0, distance]:
                cell = (cell_x + dx, cell_y + dy)
                if cell in self._cells:
                    # Filter boids in this cell using the bitmask
                    neighbors.extend(
                        [other_boid for other_boid in self._cells[cell] 
                         if other_boid._group_mask & target_mask]
                    )
        return neighbors
    
    def get_boid_count_in_cell(self, cell):
        """Return the total number of boids in a cell."""
        return len(self._cells[cell])