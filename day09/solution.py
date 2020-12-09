from typing import Tuple, Set, List
from enum import Enum, auto
from itertools import combinations


CommandType = Tuple[str, int]


def get_parsed_lines() -> List[int]:
    with open("input.txt") as f:
        return list(map(int, f.readlines()))


def find_first_error(numbers: List[int], preamble: int) -> int:
    for i in range(preamble, len(numbers)):
        if not any(sum(c) == numbers[i]
                   for c in combinations(numbers[i-preamble:i], r=2)):
            return numbers[i]
    raise ValueError("Value not found")


def find_encryption_weakness(numbers: List[int], first_error: int) -> int:
    for i in range(len(numbers)):
        for j in range(1, len(numbers) + 1):
            if j <= i:
                continue
            slice = numbers[i:j]
            if sum(slice) == first_error:
                return min(slice) + max(slice)
    raise ValueError("Weakness not found")


def main():
    numbers = get_parsed_lines()
    first_error = find_first_error(numbers, 25)
    # part 1
    print(first_error)
    # part 2
    print(find_encryption_weakness(numbers, first_error))


if __name__ == "__main__":
    main()
