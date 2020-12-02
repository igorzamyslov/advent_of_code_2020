import itertools
import operator
from functools import reduce
from typing import List


def read_input():
    with open("input.txt") as f:
        data = list(map(int, f.readlines()))
    return data


def find_answer(input_list: List, combination_length: int):
    for combination in itertools.combinations(input_list, combination_length):
        if sum(combination) == 2020:
            return reduce(operator.mul, combination, 1)
    raise ValueError


if __name__ == "__main__":
    # part 1
    print(find_answer(read_input(), 2))
    # part 2
    print(find_answer(read_input(), 3))
