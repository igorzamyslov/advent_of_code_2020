from __future__ import annotations

from copy import deepcopy
from typing import List, Dict


ParsedInputType = Dict[int, List[int]]


def get_parsed_input() -> ParsedInputType:
    with open("input.txt") as f:
        return {int(n): [i] for i, n in enumerate(f.readline().split(","))}


def solve_part_one(parsed_input: ParsedInputType, end_turn: int = 2020):
    game_dict = deepcopy(parsed_input)
    turn = len(game_dict)
    last_number = list(game_dict.keys())[-1]
    while turn < end_turn:
        if len(game_dict[last_number]) == 1:
            last_number = 0
        else:
            previous_turn, last_turn = game_dict[last_number][-2:]
            last_number = last_turn - previous_turn
        game_dict.setdefault(last_number, []).append(turn)
        turn += 1
    return last_number


def solve_part_two(parsed_input: ParsedInputType):
    return solve_part_one(parsed_input, end_turn=30000000)


def main():
    # data
    parsed_input = get_parsed_input()
    # part 1
    print(solve_part_one(parsed_input))
    # part 2
    print(solve_part_two(parsed_input))


if __name__ == "__main__":
    main()
