from typing import List
from itertools import chain

def get_groups() -> List[List[str]]:
    with open("input.txt") as f:
        return [group.split("\n") for group in f.read().split("\n\n")]

def count_unique_answers_per_group(groups) -> int:
    return sum(len(set(chain(*group))) for group in groups)

def count_common_answers_per_group(groups) -> int:
    return sum(len(set.intersection(*(set(person) for person in group)))
               for group in groups)

def main():
    input_groups = get_groups()
    # part 1
    print(count_unique_answers_per_group(input_groups))
    # part 2
    print(count_common_answers_per_group(input_groups))


if __name__ == "__main__":
    main()