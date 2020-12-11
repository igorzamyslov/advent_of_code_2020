from __future__ import annotations
from dataclasses import dataclass, replace
from copy import deepcopy
from typing import List, Tuple, Dict, Optional
from itertools import groupby


def get_parsed_lines() -> List[str]:
    with open("input.txt") as f:
        return f.readlines()


@dataclass(frozen=True)
class Seat:
    x: int
    y: int
    occupied: bool

    def __str__(self) -> str:
        return "#" if self.occupied else "L"


@dataclass(frozen=True)
class Map:
    seats: Tuple[Seat, ...]
    _adjacency_map: Optional[Dict[Tuple[int, int], List[int]]] = None
    # ^ - stupid solution

    def __post_init__(self):
        # in case object is created via a copy / replace
        # skip the adjacency map generation
        if not self._adjacency_map:
            object.__setattr__(self, "_adjacency_map",
                               {(s.x, s.y): self._get_adjacent_indexes(s)
                                for s in self.seats})

    def __str__(self) -> str:
        max_x = max(s.x for s in self.seats)
        output_string = ""
        for _, line in groupby(sorted(self.seats, key=lambda s: (s.y, s.x)),
                               key=lambda s: s.y):
            previous_x = -1
            for seat in line:
                output_string += "." * (seat.x - previous_x - 1)
                output_string += str(seat)
                previous_x = seat.x
            output_string += "." * (max_x - previous_x)
            output_string += "\n"
        return output_string

    def _get_adjacent_indexes(self, seat: Seat) -> List[int]:
        adjacent_indexes: List[int] = []
        for i, map_seat in enumerate(self.seats):
            if ((map_seat.x != seat.x or map_seat.y != seat.y)
                    and abs(map_seat.x - seat.x) <= 1
                    and abs(map_seat.y - seat.y) <= 1):
                adjacent_indexes.append(i)
        return adjacent_indexes

    def get_adjacent_seats(self, seat: Seat) -> List[Seat]:
        adjacent_seats: List[Seat] = []
        for i in self._adjacency_map[(seat.x, seat.y)]:
            adjacent_seats.append(self.seats[i])
        return adjacent_seats

    def create_new_seat_state(self, seat: Seat) -> Seat:
        """ Create new state of the seat based on the set of rules """
        adjacent_seats = self.get_adjacent_seats(seat)
        if seat.occupied:
            if sum(s.occupied for s in adjacent_seats) >= 4:
                return replace(seat, occupied=False)
        else:
            if all(not s.occupied for s in adjacent_seats):
                return replace(seat, occupied=True)
        return deepcopy(seat)

    def create_new_map_state(self) -> Map:
        """ Create new state of the map based on the set of rules """
        return Map(seats=tuple(map(self.create_new_seat_state, self.seats)),
                   _adjacency_map=self._adjacency_map)


def stabilize_map(map: Map, print_maps: bool = False) -> Map:
    new_state = map.create_new_map_state()
    while map != new_state:
        if print_maps:
            print(map)
            print()
        map = new_state
        new_state = map.create_new_map_state()
    return new_state


def create_map_from_lines(lines: List[str]) -> Map:
    seats: List[Seat] = []
    for y, line in enumerate(lines):
        for x, cell in enumerate(line.strip()):
            if cell == ".":
                continue
            seats.append(Seat(x=x, y=y, occupied=(cell == "#")))
    return Map(seats=tuple(seats))


def main():
    # data
    seat_map = create_map_from_lines(get_parsed_lines())
    # part 1
    stabilized_map = stabilize_map(seat_map)
    print(sum(s.occupied for s in stabilized_map.seats))
    # part 2


if __name__ == "__main__":
    main()