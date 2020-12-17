from __future__ import annotations

import re
from itertools import product, repeat
from typing import List, Dict, Tuple, Set
from functools import reduce
from copy import deepcopy
import operator
from collections import defaultdict

from matplotlib import colors


CoordsType = Tuple[int, ...]  # x, y, z, ...
ParsedInputType = Dict[CoordsType, bool]  # .-False, #-True


def get_parsed_input(dimensions: int) -> ParsedInputType:
    with open("input.txt") as f:
        lines = f.readlines()
    output = defaultdict(lambda: False)
    for x, line in enumerate(lines):
        for y, character in enumerate(line.strip()):
            output[(x, y, *repeat(0, dimensions - 2))] = (character == "#")
    return output


def count_active_neighbours(coords: CoordsType, pocket: ParsedInputType,
                            dimensions: int) -> int:
    """ 
    Function that counts active neighbour cubes in the pocket dimention.
    Given that pocket dimension is a default dict, as a bonus - creates new layer
    Stupid and slow, I know, sue me!
    """
    return sum(pocket[tuple(map(sum, zip(coords, c)))]
               for c in filter(lambda c: sum(map(abs, c)), 
                               product(range(-1, 2), repeat=dimensions)))


def solve_part_one(parsed_input: ParsedInputType, dimensions: int = 3):
    pocket_dimension = deepcopy(parsed_input)
    # create new outer layer
    for key in list(pocket_dimension.keys()):
        count_active_neighbours(key, pocket_dimension, dimensions)

    for _ in range(6):
        changes = [] 
        for key in list(pocket_dimension.keys()):
            active_neighbours = count_active_neighbours(key, pocket_dimension, dimensions)
            if pocket_dimension[key]:
                if active_neighbours not in [2, 3]:
                    changes.append((key, False))
            else:
                if active_neighbours == 3:
                    changes.append((key, True))
        for key, value in changes:
            pocket_dimension[key] = value
        # plot(pocket_dimension)
    return sum(pocket_dimension.values())


def solve_part_two(parsed_input: ParsedInputType):
    return solve_part_one(parsed_input, dimensions=4)


def main():
    # data
    pocket_3_dimension = get_parsed_input(3)
    pocket_4_dimension = get_parsed_input(4)
    # part 1
    print(solve_part_one(pocket_3_dimension))
    # part 2
    print(solve_part_two(pocket_4_dimension))


if __name__ == "__main__":
    main()
