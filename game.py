import numpy as np

from boat import Boat
from game_data import *


class Game:
    def __init__(self):
        self.my_grid = np.full(GRID_SIZE, GridCellType.water, dtype=GridCellType)
        self.my_guessed = np.full(GRID_SIZE, GridCellType.water, dtype=GridCellType)

        self.my_boats = []

    def place_one_boat(self, boat_type: BoatType, pos_head: tuple, orientation: Orientation):
        if orientation == Orientation.horizontal:
            # make sure boat fits in the grid
            if pos_head[0] + boat_type.value - 1 <= GRID_SIZE[0] - 1 and pos_head[0] >= 0 and pos_head[1] >= 0:
                # make sure boat does not cross another boat
                free_space = True
                for i in range(boat_type.value):
                    if self.my_grid[pos_head[0]][pos_head[1] + i] != GridCellType.water:
                        free_space = False
                        print("bato ds traj bro")
                        break
                if free_space:
                    self.my_boats.append(Boat(boat_type, pos_head, orientation))
                    for i in range(boat_type.value):
                        self.my_grid[pos_head[0]][pos_head[1] + i] = GridCellType.boat

        elif orientation == Orientation.vertical:
            # make sure boat fits in the grid
            if pos_head[1] + boat_type.value - 1 <= GRID_SIZE[1] - 1 and pos_head[1] >= 0 and pos_head[1] >= 0:
                # make sure boat does not cross another boat
                free_space = True
                for i in range(boat_type.value):
                    if self.my_grid[pos_head[0] + i][pos_head[1]] != GridCellType.water:
                        free_space = False
                        print("bato ds traj bro")
                        break
                if free_space:
                    self.my_boats.append(Boat(boat_type, pos_head, orientation))
                    for i in range(boat_type.value):
                        self.my_grid[pos_head[0] + i][pos_head[1]] = GridCellType.boat
