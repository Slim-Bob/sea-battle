from __future__ import annotations
from constants import HitStatus, CellStatus
from player import Player, AI


def clear_screen() -> None:
    # os.system("cls")
    print("\n" * 10)


if __name__ == "__main__":
    try:
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
                print(f'{player1.name} ранил: {cell}')
                player1.set_move(cell, CellStatus.HIT)
            elif status == HitStatus.KILL:
                print(f'{player1.name} убил: {cell}')
                player1.set_move(cell, CellStatus.HIT)
                if player2.played_enough():
                    continue
                else:
                    clear_screen()
                    print('Победа' if isinstance(player1, Player) else 'Поражение')
                    player1.print_board()
                    exit()
            else:
                print(f'{player1.name} промазал: {cell}')
                player1.set_move(cell, CellStatus.MISS)
                if isinstance(player1, Player):
                    player1 = ai
                    player2 = pl
                else:
                    player1 = pl
                    player2 = ai
    except Exception:
        print("Dce")
