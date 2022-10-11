from __future__ import annotations
from constants import CellStatus, HitStatus
from ship import Ship, ShipOne, ShipTwo, ShipThree


class Board:
    MAX_WIDTH = 6
    MAX_HEIGHT = 6

    COUNT_SHIP_ONE = 4
    COUNT_SHIP_TWO = 2
    COUNT_SHIP_THREE = 1

    _board = []
    _count_ship_one = 0
    _count_ship_two = 0
    _count_ship_tree = 0

    _ships = []
    _kill_ships = []

    def generate_ships(self):
        pass

    @property
    def Ships(self) -> list(Ship):
        return self._ships

    @property
    def Kills(self) -> list(Ship):
        return self._kill_ships

    def print(self):
        pass

    def Hit(self, cell: tuple) -> HitStatus:
        if not self.check_cell(cell):
            raise Exception

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
            for ship in self.ships:
                if cell in ship.get_coordinates():
                    new_val = ship.set_his(cell)
                    if new_val == HitStatus.KILL:
                        self._kill_ships.append(ship)
                        self._ships.remove(ship)
                        self.change_cell(cell, CellStatus.HIT)
                    if new_val == HitStatus.HIT:
                        self.change_cell(cell, CellStatus.HIT)
                    break
            return new_val

    def _get_val_cell(self, cell: tuple) -> CellStatus:
        return self._board[cell[0]][cell[1]]

    @Ships.setter
    def ships(self, ships: list(Ship)):
        if self._check_ships(ships):
            self._ships.extend(ships)

            for ship in ships:
                for coordinate in ship.get_coordinates():
                    self.change_cell(coordinate, CellStatus.SHIP)

    def check_count_ships(self) -> bool:
        count_one = 0
        count_two = 0
        count_three = 0

        for ship in self.ships:
            if ship is ShipOne:
                count_one += 1
            if ship is ShipTwo:
                count_two += 1
            if ship is ShipThree:
                count_three += 1

        return all([count_one != Board.COUNT_SHIP_ONE,
                    count_two != Board.COUNT_SHIP_TWO,
                    count_three != Board.COUNT_SHIP_THREE])

    def __init__(self):
        self._board = [[CellStatus.EMPTY for y in range(Board.MAX_HEIGHT)] for x in range(Board.MAX_WIDTH)]
        self._ships = []

    def change_cell(self, coordinate: tuple, val: CellStatus):
        if self.check_coordinate(coordinate):
            self._board[coordinate[0]][coordinate[1]] = val

    def check_cell(self, coordinate: tuple) -> bool:
        if self._board[coordinate[0]][coordinate[1]] == CellStatus.EMPTY:
            return True
        else:
            return False

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

    def _check_ships(self, ships: list(Ship)) -> bool:
        adjacents = set()

        for ship in ships:
            adjacents.union(ship.get_adjacent())

        for ship in self.ships:
            adjacents.union(ship.get_adjacent())

        for ship in ships:
            coordinates = ship.get_coordinates()

            if adjacents in coordinates:
                return True

        return False

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
    def next_two_adjacent(coordinate: tuple) -> set:

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
    pass
