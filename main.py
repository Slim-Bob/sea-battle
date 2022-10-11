from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from constants import HitStatus, CellStatus


class Player(ABC):
    @abstractmethod
    def print_board(self):
        pass

    @abstractmethod
    def set_his(self, coordinate: tuple) -> HitStatus:
        pass

    @abstractmethod
    def move(self) -> tuple:
        pass

    @abstractmethod
    def set_move(self, coordinate: tuple, hitStatus: HitStatus):
        pass

    @abstractmethod
    def is_ships(self) -> bool:
        pass








if __name__ == "__main__":

    print("Test")
