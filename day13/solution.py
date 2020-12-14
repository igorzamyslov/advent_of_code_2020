from __future__ import annotations

import math
import sympy
from typing import Dict, List, Optional, Tuple, Union


def get_parsed_lines() -> Tuple[int, List[str]]:
    with open("input.txt") as f:
        min_timestamp, buses = f.readlines()
        return int(min_timestamp), buses.split(",")


def get_enumerated_valid_buses(buses: List[str]) -> List[Tuple[int, int]]:
    return [(i, int(b)) for i, b in enumerate(buses) if b != "x"]


def solve_part_one(min_timestamp: int, valid_buses: List[int]) -> int:
    diff, vb = min(((vb - min_timestamp % vb), vb) for vb in valid_buses)
    return diff * vb


def solve_part_two(enumerated_valid_buses: List[Tuple[int, int]]) -> int:
    x, i, j, k = sympy.symbols("x, i, j, k")
    s = sympy.linsolve([i*x - 17, j*x + 2*j - 13, k*x + 3*k - 19], [x, i, j, k])
    print(s)


def main():
    # data
    min_timestamp, buses = get_parsed_lines()
    enumerated_valid_buses = get_enumerated_valid_buses(buses)
    # part 1
    valid_buses = [b for i, b in enumerated_valid_buses]
    print(solve_part_one(min_timestamp, valid_buses))
    # part 2
    print(solve_part_two(enumerated_valid_buses))


if __name__ == "__main__":
    main()
