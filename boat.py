from game_data import BoatType, Orientation
from gridcell import *


class Boat:
    def __init__(self, boat_type: BoatType, pos_head: tuple, orientation: Orientation):
        self.type = boat_type
        self.length = boat_type.value
        self.orientation = orientation
        self.cells = list()
        self.set_position(pos_head)

    def is_drowned(self):
        res = True
        for cell in self.cells:
            if cell.state == BoatCellState.safe:
                res = False
                break
        return res

    def set_position(self, pos_head: tuple):
        for i in range(self.length):
            if self.orientation == Orientation.vertical:
                self.cells.append(ShipCell((pos_head[0], pos_head[1] + i)))
            else:
                self.cells.append(ShipCell((pos_head[0] + i, pos_head[1])))

    def __str__(self):
        return f"{self.type}: Alive" if not self.is_drowned() else f"{self.type}: Drowned"
