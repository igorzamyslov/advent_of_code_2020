from __future__ import annotations
from dataclasses import dataclass, replace
from copy import deepcopy
from typing import List, Tuple, Type
from itertools import groupby, product
from abc import ABC, abstractmethod


def get_parsed_lines() -> List[str]:
    with open("input.txt") as f:
        return f.readlines()


@dataclass(frozen=True)
class Seat:
    x: int
    y: int
    occupied: bool

    def __str__(self) -> str:
        """ Create string representation of the seat """
        return "#" if self.occupied else "L"


@dataclass(frozen=True)
class Map:
    seats: Tuple[Seat, ...]

    def __post_init__(self):
        """ Init field and dimensions """
        field = {}
        max_x = 0
        max_y = 0
        for seat in self.seats:
            field.setdefault(seat.x, {})
            field[seat.x][seat.y] = seat
            max_x = max(max_x, seat.x)
            max_y = max(max_y, seat.y)
        object.__setattr__(self, "_field", field)
        object.__setattr__(self, "_max_x", max_x)
        object.__setattr__(self, "_max_y", max_y)

    @staticmethod
    def from_lines(lines: List[str]) -> Map:
        seats: List[Seat] = []
        for y, line in enumerate(lines):
            for x, cell in enumerate(line.strip()):
                if cell == ".":
                    continue
                seats.append(Seat(x=x, y=y, occupied=(cell == "#")))
        return Map(seats=tuple(seats))

    def __str__(self) -> str:
        """ Create string representation of the map """
        output_string = ""
        for _, line in groupby(sorted(self.seats, key=lambda s: (s.y, s.x)),
                               key=lambda s: s.y):
            previous_x = -1
            for seat in line:
                output_string += "." * (seat.x - previous_x - 1)
                output_string += str(seat)
                previous_x = seat.x
            output_string += "." * (self._max_x - previous_x)
            output_string += "\n"
        return output_string

    def count_occupied_seats(self) -> int:
        return sum(s.occupied for s in self.seats)


class BaseMapStabilizer(ABC):
    tolerance: int

    def __init__(self, map_obj: Map) -> None:
        self.map = map_obj
        self.stabilized = False

    @abstractmethod
    def get_relevant_seats(self, seat: Seat) -> List[Seat]:
        """ Get relevant seats for create_new_seat_state """

    def create_new_seat_state(self, seat: Seat) -> Seat:
        """ Create new state of the seat based on the set of rules """
        relevant_seats = self.get_relevant_seats(seat)
        if seat.occupied:
            if sum(s.occupied for s in relevant_seats) >= self.tolerance:
                return replace(seat, occupied=False)
        else:
            if all(not s.occupied for s in relevant_seats):
                return replace(seat, occupied=True)
        return deepcopy(seat)

    def create_new_map_state(self) -> Map:
        """ Create new state of the map based on the set of rules """
        return Map(seats=tuple(map(self.create_new_seat_state, self.map.seats)))

    def stabilize(self, print_maps: bool = False):
        new_state = self.create_new_map_state()
        while self.map != new_state:
            if print_maps:
                print(self.map)
                print()
            self.map = new_state
            new_state = self.create_new_map_state()
        self.stabilized = True


class PartOneMapStabilizer(BaseMapStabilizer):
    """ Stabilisation based on the adjacent seats """
    tolerance = 4

    def get_relevant_seats(self, seat: Seat) -> List[Seat]:
        """ Get adjacent seats """
        adjacent_seats: List[Seat] = []
        for delta_x, delta_y in product((-1, 0, 1), repeat=2):
            if delta_x == delta_y and delta_y == 0:
                continue
            try:
                adjacent_seats.append(self.map._field[seat.x+delta_x][seat.y+delta_y])
            except KeyError:
                continue
        return adjacent_seats


class PartTwoMapStabilizer(BaseMapStabilizer):
    """ Stabilisation based on the visible seats """
    tolerance = 5

    def _get_coordinates(self, seat: Seat, dx: int, dy: int) -> Tuple[int, int]:
        x = seat.x + dx
        if x < 0 or x > self.map._max_x:
            raise ValueError
        y = seat.y + dy
        if y < 0 or y > self.map._max_y:
            raise ValueError
        return x, y

    def get_relevant_seats(self, seat: Seat) -> List[Seat]:
        """ Get visible seats """
        visible_seats: List[Seat] = []
        for vector_x, vector_y in product((-1, 0, 1), repeat=2):
            if vector_x == vector_y and vector_y == 0:
                continue

            delta_x = vector_x
            delta_y = vector_y
            while True:
                try:
                    x, y = self._get_coordinates(seat, delta_x, delta_y)
                except ValueError:
                    break

                try:
                    visible_seat = self.map._field[x][y]
                except KeyError:
                    delta_x += vector_x
                    delta_y += vector_y
                    continue
                visible_seats.append(visible_seat)
                break
        return visible_seats


def print_solution(map_obj: Map, stabilizer_cls: Type[BaseMapStabilizer]):
    stabilizer = stabilizer_cls(map_obj)
    stabilizer.stabilize()
    print(stabilizer.map.count_occupied_seats())


def main():
    # data
    seat_map = Map.from_lines(get_parsed_lines())
    # part 1
    print_solution(seat_map, PartOneMapStabilizer)
    # part 2
    print_solution(seat_map, PartTwoMapStabilizer)


if __name__ == "__main__":
    main()
