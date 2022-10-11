from __future__ import annotations
from abc import ABC, abstractmethod
from constants import HitStatus
from board import Board


class Ship(ABC):
    __coordinates = dict()
    __hit = 0

    def __init__(self, coordinates: list(tuple)):
        self.__hit = len(coordinates)
        self.__coordinates = {}

        for coordinate in coordinates:
            if not Board.check_coordinate(coordinate):
                raise Exception

            self.__coordinates[coordinate] = True

        self.check_create(coordinates)

    def set_his(self, coordinate: tuple) -> HitStatus:
        try:
            if self.__coordinates.get(coordinate):
                self.__coordinates[coordinate] = False
                self.__hit -= 1
                return HitStatus.HIT if self.__hit > 0 else HitStatus.KILL
            else:
                return HitStatus.MISS
        except Exception as e:
            return HitStatus.MISS

    def get_coordinates(self) -> set:
        return set(self.__coordinates.keys())

    @abstractmethod
    def check_create(self, coordinates: list):
        pass

    def get_adjacent(self) -> set:
        coordinates = []

        for coordinate in self.__coordinates.keys():
            coordinates.extend(list(Board.next_adjacent(coordinate)))

        return set(coordinates) - self.get_coordinates()


class ShipOne(Ship):
    def check_create(self, coordinates: list):
        if len(coordinates) != 1:
            raise Exception

    def __str__(self):
        return f'Однопалубник ${self.__coordinates}'

class ShipTwo(Ship):
    def check_create(self, coordinates: list):
        if len(set(coordinates)) != 2:
            raise Exception

        adjacents = set(Board.next_adjacent(coordinates[0]))

        if coordinates[1] not in adjacents:
            raise Exception

    def __str__(self):
        return f'Двухпалубник ${self.__coordinates}'

class ShipThree(Ship):
    def check_create(self, coordinates: list):
        if len(set(coordinates)) != 3:
            raise Exception

        for adjacents in Board.next_two_adjacent(coordinates[0]):
            if coordinates[1] in adjacents and coordinates[2] in adjacents:
                return

        for adjacents in Board.next_two_adjacent(coordinates[1]):
            if coordinates[0] in adjacents and coordinates[2] in adjacents:
                return

        for adjacents in Board.next_two_adjacent(coordinates[2]):
            if coordinates[0] in adjacents and coordinates[1] in adjacents:
                return

        raise Exception

    def __str__(self):
        return f'Трехпалубник ${self.__coordinates}'


if __name__ == "__main__":
    s1 = ShipOne([(0, 1)])
    s2 = ShipOne([(2, 3)])
    s3 = ShipOne([(3, 4)])
    s4 = ShipOne([(5, 6)])

    # s5 = ShipOne([(5, 6),(3, 1)])
    s6 = ShipTwo([(5, 6), (4, 6)])

    print(s1.set_his((0, 1)))
    print(s2.set_his((0, 1)))

    s7 = ShipThree([(5, 6), (4, 6), (3, 6)])
    s8 = ShipThree([(5, 6), (4, 6), (1, 6)])

    # t1 = s1.get_adjacent()
    # t3 = s3.get_adjacent()
    t6 = s6.get_adjacent()
