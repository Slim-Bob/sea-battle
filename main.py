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


def clear_screen() -> None:
    # os.system("cls")
    print("\n" * 10)


def power_transmission(plr1: PlayerAbstract, plr2: PlayerAbstract, plv: Player, aiv: AI):
    if isinstance(plr1, Player):
        plr1 = aiv
        plr2 = plv
    else:
        plr1 = plv
        plr2 = aiv


if __name__ == "__main__":
    pl = Player()
    ai = AI()

    player1 = pl
    player2 = ai

    while True:
        if isinstance(player1, Player):
            clear_screen()
            print('Ваш ход')
            player1.print_board()

        cell = player1.move()
        status = player2.set_his(cell)

        if status == HitStatus.HIT:
            player1.set_move(cell, CellStatus.HIT)
        elif status == HitStatus.KILL:
            player1.set_move(cell, CellStatus.HIT)
            if player2.played_enough():
                continue
                #power_transmission(player1, player2, ai, pl)
            else:
                clear_screen()
                print('Победа' if isinstance(player1, Player) else 'Поражение')
                player1.print_board()
                exit()
        else:
            player1.set_move(cell, CellStatus.MISS)
            #power_transmission(player1, player2, ai, pl)
            if isinstance(player1, Player):
                player1 = ai
                player2 = pl
            else:
                player1 = pl
                player2 = ai
