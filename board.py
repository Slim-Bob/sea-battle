from __future__ import annotations
from constants import CellStatus, HitStatus
import ship


class Board:
    MAX_WIDTH = 6
    MAX_HEIGHT = 6

    COUNT_SHIP_ONE = 4
    COUNT_SHIP_TWO = 2
    COUNT_SHIP_THREE = 1

    _board = []
    _count_ship_one = 0
    _count_ship_two = 0
    _count_ship_three = 0

    _ships = []
    _kill_ships = []

    @property
    def count_ship_one(self):
        return self._count_ship_one

    @property
    def count_ship_two(self):
        return self._count_ship_two

    @property
    def count_ship_three(self):
        return self._count_ship_three

    def generate_ships(self):
        pass

    @property
    def ships(self) -> list(ship.Ship):
        return self._ships

    @property
    def kills(self) -> list(ship.Ship):
        return self._kill_ships

    def print(self):
        line = "y|x"

        for x in range(Board.MAX_WIDTH):
            line += f"\t{x}"

        print(line)

        for y in range(Board.MAX_HEIGHT):
            line = f"{y}"
            for x in range(Board.MAX_WIDTH):
                line += f"\t{self._board[y][x].value}"
            print(line)

    def hit(self, cell: tuple) -> HitStatus:
        val_cell = self._get_val_cell(cell)
        new_val = HitStatus.MISS

        if val_cell == CellStatus.HIT:
            raise Exception
        if val_cell == CellStatus.MISS:
            raise Exception
        if val_cell == CellStatus.EMPTY:
            self.change_cell(cell, CellStatus.MISS)
            return HitStatus.MISS
        if val_cell == CellStatus.SHIP:
            for shp in self.ships:
                if cell in shp.get_coordinates():
                    new_val = shp.set_his(cell)
                    if new_val == HitStatus.KILL:
                        self._kill_ships.append(shp)
                        self._ships.remove(shp)
                        self.change_cell(cell, CellStatus.HIT)
                    if new_val == HitStatus.HIT:
                        self.change_cell(cell, CellStatus.HIT)
                    break
            return new_val

    def _get_val_cell(self, cell: tuple) -> CellStatus:
        return self._board[cell[0]][cell[1]]

    def set_ships(self, ships: list(ship.Ship)):
        if self.check_ships(ships):
            self._ships.extend(ships)

            for shp in ships:
                if isinstance(shp, ship.ShipOne):
                    self._count_ship_one += 1
                if isinstance(shp, ship.ShipTwo):
                    self._count_ship_two += 1
                if isinstance(shp, ship.ShipThree):
                    self._count_ship_three += 1

                for coordinate in shp.get_coordinates():
                    self.change_cell(coordinate, CellStatus.SHIP)
        else:
            raise Exception

    def check_count_ships(self) -> bool:
        return all([self._count_ship_one != Board.COUNT_SHIP_ONE,
                    self._count_ship_two != Board.COUNT_SHIP_TWO,
                    self._count_ship_three != Board.COUNT_SHIP_THREE])

    def __init__(self):
        self._board = [[CellStatus.EMPTY for y in range(Board.MAX_HEIGHT)] for x in range(Board.MAX_WIDTH)]
        self._ships = []

    def change_cell(self, coordinate: tuple, val: CellStatus):
        if self.check_coordinate(coordinate):
            self._board[coordinate[0]][coordinate[1]] = val

    def get_empty_cells(self) -> list(tuple):
        empty = []

        for y in range(Board.MAX_HEIGHT):
            for x in range(Board.MAX_WIDTH):
                if self._board[y][x] == CellStatus.EMPTY:
                    empty.append((y, x))

        return empty

    def __iter__(self):
        for y in range(Board.MAX_HEIGHT):
            for x in range(Board.MAX_WIDTH):
                yield self._board[y][x]

    def next_line(self):
        for y in range(Board.MAX_HEIGHT):
            yield self._board[y]

    def check_ships(self, ships: list(ship.Ship)) -> bool:
        adjacents_board = set()
        for shp in self._ships:
            adjacents_board = adjacents_board.union(shp.get_adjacent())
            adjacents_board = adjacents_board.union(shp.get_coordinates())

        adjacents = set()
        for check_shp in ships:
            adjacents.clear()

            for shp in ships:
                if check_shp != shp:
                    adjacents = adjacents.union(shp.get_adjacent())
                    adjacents = adjacents.union(shp.get_coordinates())

            adjacents = adjacents.union(adjacents_board)
            for coordinate in check_shp.get_coordinates():
                if coordinate in adjacents:
                    return False

        return True

    @staticmethod
    def check_coordinate(coordinate: tuple) -> bool:
        if len(coordinate) != 2:
            raise Exception

        if all([coordinate[0] >= 0,
                coordinate[0] <= Board.MAX_HEIGHT,
                coordinate[1] >= 0,
                coordinate[1] <= Board.MAX_WIDTH]):
            return True
        else:
            return False

    @staticmethod
    def next_adjacent(coordinate: tuple) -> tuple:

        adjacent = (coordinate[0] - 1, coordinate[1])
        if Board.check_coordinate(adjacent):
            yield adjacent

        adjacent = (coordinate[0] + 1, coordinate[1])
        if Board.check_coordinate(adjacent):
            yield adjacent

        adjacent = (coordinate[0], coordinate[1] - 1)
        if Board.check_coordinate(adjacent):
            yield adjacent

        adjacent = (coordinate[0], coordinate[1] + 1)
        if Board.check_coordinate(adjacent):
            yield adjacent

    @staticmethod
    def next_two_adjacent(coordinate: tuple) -> set(tuple):

        adjacent1 = (coordinate[0] - 1, coordinate[1])
        adjacent2 = (coordinate[0] - 2, coordinate[1])
        if Board.check_coordinate(adjacent1) and Board.check_coordinate(adjacent2):
            yield {adjacent1, adjacent2}

        adjacent1 = (coordinate[0] + 1, coordinate[1])
        adjacent2 = (coordinate[0] + 2, coordinate[1])
        if Board.check_coordinate(adjacent1) and Board.check_coordinate(adjacent2):
            yield {adjacent1, adjacent2}

        adjacent1 = (coordinate[0], coordinate[1] - 1)
        adjacent2 = (coordinate[0], coordinate[1] - 2)
        if Board.check_coordinate(adjacent1) and Board.check_coordinate(adjacent2):
            yield {adjacent1, adjacent2}

        adjacent1 = (coordinate[0], coordinate[1] + 1)
        adjacent2 = (coordinate[0], coordinate[1] + 2)
        if Board.check_coordinate(adjacent1) and Board.check_coordinate(adjacent2):
            yield {adjacent1, adjacent2}


if __name__ == "__main__":
    board = Board()
    #ships = [ship.ShipTwo([(0, 0), (0, 1)]), ship.ShipOne([(1, 2)])]
    #ships = [ship.ShipTwo([(0, 0), (0, 1)])]
    ships = [ship.ShipThree([(1, 4), (2, 4), (3, 4)])]
    try:
        board.set_ships(ships)
    except Exception:
        pass

    ships = [ship.ShipTwo([(3, 5), (4, 5)])]
    try:
        board.set_ships(ships)
    except Exception:
        pass
    board.print()

    print("---")

    board.hit((0, 0))
    board.print()

    print("---")

    board.hit((1, 2))
    board.print()
    print("---")
    for kill_ship in board.kills:
        print(kill_ship)