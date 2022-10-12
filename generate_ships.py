from __future__ import annotations
import ship
import board
from random import randrange


def generate_ships(brd: board.Board):
    for i in range(10):
        new_board = board.Board()
        new_board.set_ships(brd.ships)

        create_ships(new_board)
        if new_board.check_count_ships():
            brd.set_ships(new_board.ships)
            return
        else:
            continue

    raise Exception


def create_ships(brd: board.Board):
    empty_cells = brd.get_empty_cells()

    while empty_cells and brd.count_ship_three < board.Board.COUNT_SHIP_THREE:
        idx_cell_rnd = randrange(0, len(empty_cells) - 1)
        rnd_cell = empty_cells[idx_cell_rnd]

        list_adjacents = list(board.Board.next_two_adjacent(rnd_cell))

        while list_adjacents:
            idx_rnd = randrange(0, len(list_adjacents) - 1)
            list_adjacents_cell = list(list_adjacents[idx_rnd])
            ship_three = ship.ShipThree([rnd_cell, list_adjacents_cell[0], list_adjacents_cell[1]])
            try:
                brd.set_ships([ship_three])
                empty_cells.remove(rnd_cell)
                empty_cells.remove(list_adjacents_cell[0])
                empty_cells.remove(list_adjacents_cell[1])
                break
            except Exception:
                list_adjacents.remove(list_adjacents_cell)
                continue

        if not list_adjacents:
            empty_cells.remove(rnd_cell)
            continue

    while empty_cells and brd.count_ship_two < board.Board.COUNT_SHIP_TWO:
        idx_cell_rnd = randrange(0, len(empty_cells) - 1)
        rnd_cell = empty_cells[idx_cell_rnd]

        list_adjacents = list(board.Board.next_adjacent(rnd_cell))

        while list_adjacents:
            if len(list_adjacents) > 1:
                idx_rnd = randrange(0, len(list_adjacents) - 1)
            else:
                idx_rnd = 0
            new_cell = list_adjacents[idx_rnd]
            ship_two = ship.ShipTwo([rnd_cell, new_cell])
            try:
                brd.set_ships([ship_two])
                empty_cells.remove(rnd_cell)
                empty_cells.remove(new_cell)
                break
            except Exception:
                list_adjacents.remove(new_cell)
                continue

        if not list_adjacents:
            try:
                empty_cells.remove(rnd_cell)
            except Exception:
                pass
            finally:
                continue

    while empty_cells and brd.count_ship_one < board.Board.COUNT_SHIP_ONE:
        if len(empty_cells) > 1:
            idx_cell_rnd = randrange(0, len(empty_cells) - 1)
        else:
            idx_cell_rnd = 0
        rnd_cell = empty_cells[idx_cell_rnd]
        ship_one = ship.ShipOne([rnd_cell])
        try:
            brd.set_ships([ship_one])
            empty_cells.remove(rnd_cell)
            continue
        except Exception:
            empty_cells.remove(rnd_cell)
            continue


if __name__ == "__main__":
    brd = board.Board()
    generate_ships(brd)
    brd.print()
