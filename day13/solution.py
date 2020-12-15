from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple, Union
from multiprocessing import Pool


def get_parsed_lines() -> Tuple[int, List[str]]:
    with open("input.txt") as f:
        min_timestamp, buses = f.readlines()
        return int(min_timestamp), buses.split(",")


def get_enumerated_valid_buses(buses: List[str]) -> List[Tuple[int, int]]:
    return [(i, int(b)) for i, b in enumerate(buses) if b != "x"]


def solve_part_one(min_timestamp: int, valid_buses: List[int]) -> int:
    diff, vb = min(((vb - min_timestamp % vb), vb) for vb in valid_buses)
    return diff * vb


def solve_part_two(enumerated_valid_buses: List[Tuple[int, int]], thread: int,
                   quit, foundit) -> int:
    max_vb, max_vb_i = max((vb, i) for i, vb in enumerated_valid_buses)
    current_number = 100000000000000 + 100000000000000 % max_vb + max_vb * thread
    while not quit.is_set():
        if all((current_number - max_vb_i + i) % vb == 0
               for i, vb in enumerated_valid_buses):
            foundit.set()
            break
        else:
            print(current_number)
            current_number += max_vb * (thread + 1)


def start_mp(enumerated_valid_buses: List[Tuple[int, int]]) -> int:
    import multiprocessing as mp
    quit = mp.Event()
    foundit = mp.Event()
    for i in range(mp.cpu_count() * 2):
        p = mp.Process(target=solve_part_two, 
                       args=(enumerated_valid_buses, i, quit, foundit))
        p.start()
    foundit.wait()
    quit.set()


def main():
    # data
    min_timestamp, buses = get_parsed_lines()
    enumerated_valid_buses = get_enumerated_valid_buses(buses)
    # part 1
    valid_buses = [b for i, b in enumerated_valid_buses]
    print(solve_part_one(min_timestamp, valid_buses))
    # part 2
    start_mp(enumerated_valid_buses)


if __name__ == "__main__":
    main()
