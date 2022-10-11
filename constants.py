from enum import Enum


class HitStatus(Enum):
    KILL = 1
    HIT = 2
    MISS = 3


class CellStatus(Enum):
    EMPTY = '0'
    MISS = 'T'
    HIT = 'X'
    SHIP = '1'
