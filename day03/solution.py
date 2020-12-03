import operator
from functools import reduce
from typing import List


def read_input() -> List[str]:
    with open("input.txt") as f:
        data = [line.strip() for line in f.readlines()]
    return data


def find_answer_part_one(right_step: int, down_step: int) -> int:
    counter = 0
    for i, line in enumerate(read_input()):
        if i == 0 or i % down_step != 0: 
            continue
        index = (right_step * i // down_step + 1) % len(line) - 1
        if line[index] == "#":
            counter += 1
    return counter


def find_answer_part_two() -> int:
    cases = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    return reduce(operator.mul, (find_answer_part_one(*c) for c in cases))


if __name__ == "__main__":
    # part 1
    print(find_answer_part_one(3, 1))
    # part 2
    print(find_answer_part_two())
