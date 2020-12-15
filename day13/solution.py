from __future__ import annotations

from typing import List, Tuple
from functools import reduce


class ChineseTheoremSolver:
    """
    Chinese theorem solver, that was acquired from
    https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
    """
    @staticmethod
    def chinese_remainder(n, a):
        sum = 0
        prod = reduce(lambda a, b: a*b, n)
        for n_i, a_i in zip(n, a):
            p = prod // n_i
            sum += a_i * ChineseTheoremSolver.mul_inv(p, n_i) * p
        return sum % prod

    @staticmethod
    def mul_inv(a, b):
        b0 = b
        x0, x1 = 0, 1
        if b == 1:
            return 1
        while a > 1:
            q = a // b
            a, b = b, a % b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += b0
        return x1


def get_parsed_lines() -> Tuple[int, List[str]]:
    with open("input.txt") as f:
        min_timestamp, buses = f.readlines()
        return int(min_timestamp), buses.split(",")


def get_enumerated_valid_buses(buses: List[str]) -> List[Tuple[int, int]]:
    return [(i, int(b)) for i, b in enumerate(buses) if b != "x"]


def solve_part_one(min_timestamp: int, valid_buses: List[int]) -> int:
    diff, vb = min(((vb - min_timestamp % vb), vb) for vb in valid_buses)
    return diff * vb


def solve_part_two(enumerated_valid_buses: List[Tuple[int, int]]):
    indexes, mods = zip(*((-i, vb) for i, vb in enumerated_valid_buses))
    return ChineseTheoremSolver.chinese_remainder(mods, indexes)


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
