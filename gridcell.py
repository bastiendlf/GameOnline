from game_data import BoatCellState, GridCellType


class GridCell:
    def __init__(self, pos):
        self.pos = pos
        self.type = GridCellType

    def set_type(self, cell_type: GridCellType):
        self.type = cell_type


class ShipCell(GridCell):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        super().set_type(GridCellType.boat)
        self.state = BoatCellState.safe

    def __str__(self):
        return str(f"Boat cell ({self.pos[0]}, {self.pos[1]}) : {self.state}")


class WaterCell(GridCell):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        super().set_type(GridCellType.water)
        self.is_touched = False

    def __str__(self):
        if self.is_touched:
            touched = "touched"
        else:
            touched = "untouched"
        return str(f"WATER ({self.pos[0]}, {self.pos[1]}) : {touched}")
