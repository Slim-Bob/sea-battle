from __future__ import annotations
from abc import ABC, abstractmethod
from constants import HitStatus, CellStatus
from board import Board
from generate_ships import generate_ships
from random import randrange


class PlayerAbstract(ABC):
    _board_own: Board = None
    _board_foe: Board = None
    _titel = ''

    @property
    def name(self):
        return self._titel

    def __init__(self):
        self._board_own = Board()
        generate_ships(self._board_own)
        self._board_foe = Board()
        self._titel = 'Test'

    def print_board(self):
        print(self._titel)

        line = "y|x"
        for x in range(Board.MAX_WIDTH):
            line += f"\t{x}"
        line += f"\t\ty|x"
        for x in range(Board.MAX_WIDTH):
            line += f"\t{x}"

        print(line)

        for y in range(Board.MAX_HEIGHT):
            line = f"{y}"
            for cell in self._board_own.next_line(y):
                line += f"\t{cell.value}"
            line += f"\t\t{y}"
            for cell in self._board_foe.next_line(y):
                line += f"\t{cell.value}"

            print(line)

    def set_his(self, coordinate: tuple) -> HitStatus:
        return self._board_own.hit(coordinate)

    @abstractmethod
    def move(self) -> tuple:
        pass

    def set_move(self, coordinate: tuple, val: CellStatus):
        self._board_foe.change_cell(coordinate, val)

    def played_enough(self) -> bool:
        return bool(self._board_own.ships)


class Player(PlayerAbstract):
    def __init__(self):
        super(Player, self).__init__()
        self._titel = 'Игрок'

    def move(self) -> tuple:
        while True:
            command = input("Укажите координаты y и x (Пример: 0 0, e - выйти): ")
            command = command.upper()

            command_list = command.split(' ')

            if command == "E":
                raise Exception
            elif len(command_list) == 2:
                try:
                    y = int(command_list[0])
                    x = int(command_list[1])
                except Exception:
                    print("К сожалению непонимаю =( Давай еще раз попробуем")
                    continue

                cell = (y, x)
                if not Board.check_coordinate(cell):
                    print("Указанные координаты выходят за границу")
                    continue

                if not cell in set(self._board_foe.get_empty_cells()):
                    print("Нужно указавыть координтаы которые еще не испльзовали")
                    continue

                return cell

            else:
                print("К сожалению непонимаю =( Давай еще раз попробуем")
                continue


class AI(PlayerAbstract):
    def __init__(self):
        super(AI, self).__init__()
        self._titel = 'Компьютер'

    def move(self) -> tuple:
        empty = self._board_foe.get_empty_cells()
        ind_rnd = randrange(0, len(empty) - 1)
        return empty[ind_rnd]