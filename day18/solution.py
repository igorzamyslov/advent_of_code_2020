from __future__ import annotations

import re
from typing import List
import operator


ParsedInputType = List[str]

OPERATORS = {
    "*": operator.mul,
    "+": operator.add,
}


def stabilise(function, value):
    previous_value = None
    while previous_value != value:
        previous_value = value
        value = function(value)
    return value


def get_parsed_input() -> ParsedInputType:
    with open("input.txt") as f:
        return [line.strip() for line in f.readlines()]


def calculate(match) -> str:
    var1, operator, var2 = match.groups()
    return str(OPERATORS[operator](int(var1), int(var2)))


def calculate_line_p1(match) -> str:
    [line] = match.groups()
    return stabilise(lambda l: re.sub(r"^(\d+) ([+*]) (\d+)", calculate, l), line)


def calculate_line_p2(match) -> str:
    [line] = match.groups()
    line = stabilise(lambda l: re.sub(r"(\d+) (\+) (\d+)", calculate, l), line)
    return stabilise(lambda l: re.sub(r"(\d+) (\*) (\d+)", calculate, l), line)


def calculate_line_with_brackets(line: str, calculate_line_function) -> int:
    previous_line = None
    while previous_line != line:
        previous_line = line
        line = re.sub(r"\(([^\(]+?)\)", calculate_line_function, line)
    return int(calculate_line_function(re.match(r"(.*)", line)))


def solve_part_one(parsed_input: ParsedInputType):
    return sum(calculate_line_with_brackets(line, calculate_line_p1)
               for line in parsed_input)


def solve_part_two(parsed_input: ParsedInputType):
    return sum(calculate_line_with_brackets(line, calculate_line_p2)
               for line in parsed_input)


def main():
    # data
    parsed_input = get_parsed_input()
    # part 1
    print(solve_part_one(parsed_input))
    # part 2
    print(solve_part_two(parsed_input))


if __name__ == "__main__":
    main()
