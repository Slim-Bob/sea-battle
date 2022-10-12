from __future__ import annotations
import ship
import board
from random import randrange


def generate_ships(brd: board.Board):
    empty_cells = brd.get_empty_cells()

    while empty_cells and brd.count_ship_three < board.Board.COUNT_SHIP_THREE:
        rnd = randrange(0, len(empty_cells) - 1)
        rnd_cell = empty_cells[rnd]
        for new_cells in board.Board.next_two_adjacent(rnd_cell):
            test = list(new_cells)
            ship_three = ship.ShipThree([rnd_cell, test[0], test[1]])
            try:
                brd.set_ships([ship_three])
                empty_cells.remove(rnd_cell)
                empty_cells.remove(test[0])
                empty_cells.remove(test[1])
                break
            except Exception:
                try:
                    empty_cells.remove(empty_cells[rnd_cell])
                except Exception:
                    pass
                continue

    while empty_cells and brd.count_ship_two < board.Board.COUNT_SHIP_TWO:
        rnd = randrange(0, len(empty_cells) - 1)
        rnd_cell = empty_cells[rnd]
        for new_cell in board.Board.next_adjacent(rnd_cell):
            ship_two = ship.ShipTwo([rnd_cell, new_cell])
            try:
                brd.set_ships([ship_two])
                empty_cells.remove(rnd_cell)
                empty_cells.remove(new_cell)
                break
            except Exception:
                try:
                    empty_cells.remove(rnd_cell)
                except Exception:
                    pass
                continue

    while empty_cells and brd.count_ship_one < board.Board.COUNT_SHIP_ONE:
        rnd_cell = randrange(0, len(empty_cells) - 1)
        ship_one = ship.ShipOne([empty_cells[rnd_cell]])
        try:
            brd.set_ships([ship_one])
            empty_cells.remove(empty_cells[rnd_cell])
            continue
        except Exception:
            empty_cells.remove(empty_cells[rnd_cell])
            continue

if __name__ == "__main__":
    brd = board.Board()
    generate_ships(brd)
    brd.print()