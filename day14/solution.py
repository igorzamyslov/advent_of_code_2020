from __future__ import annotations

import re
import itertools
from typing import Dict, List, Optional, Tuple, Union


def get_parsed_lines() -> List[Union[str, Tuple[int, int]]]:
    regex = r"mem\[(\d+?)\] = (\d+)"
    with open("input.txt") as f:
        output = []
        for line in f.readlines():
            line = line.strip()
            if line.startswith("mask"):
                output.append(line[7:])
            else:
                output.append(tuple(map(int, re.match(regex, line).groups())))
        return output


def get_parsed_masks(mask: str) -> Tuple[int, int]:
    """ Returns 2 masks -> 0-mask for logical AND and 1-mask for logical OR """
    return int(mask.replace("X", "1"), 2), int(mask.replace("X", "0"), 2)


def get_possible_masks(mask: str) -> List[Tuple[int, int]]:
    float_indexes = [i for i, c in enumerate(mask) if c == "X"]
    if not float_indexes:
        return [get_parsed_masks(mask)]
    output = []
    for combination in itertools.product("10", repeat=len(float_indexes)):
        new_mask = "X" * len(mask)
        for float_index, new_value in zip(float_indexes, combination):
            new_mask = new_mask[:float_index] + new_value + new_mask[float_index+1:]
        output.append(get_parsed_masks(new_mask))
    return output


def solve_part_one(parsed_input):
    address_space = {}
    and_mask = None
    or_mask = None
    for entry in parsed_input:
        if isinstance(entry, str):
            and_mask, or_mask = get_parsed_masks(entry)
        else:
            address, value = entry
            address_space[address] = value & and_mask | or_mask
    return sum(address_space.values())


def solve_part_two(parsed_input):
    address_space = {}
    masks = []
    for entry in parsed_input:
        if isinstance(entry, str):
            _, original_or_mask = get_parsed_masks(entry)
            masks = get_possible_masks(entry)
        else:
            address, value = entry
            for and_mask, or_mask in masks:
                new_address = (address | original_or_mask) & and_mask | or_mask
                address_space[new_address] = value
    return sum(address_space.values())


def main():
    # data
    parsed_input = get_parsed_lines()
    # part 1
    print(solve_part_one(parsed_input))
    # part 2
    print(solve_part_two(parsed_input))


if __name__ == "__main__":
    main()
