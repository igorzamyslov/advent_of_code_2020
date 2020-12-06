from typing import List, Tuple

def get_answers() -> List[Tuple[str, ...]]:
    with open("input.txt") as f:
        return [tuple(person for person in group.split("\n")) 
                for group in f.read().split("\n\n")]

def count_unique_answers_per_group() -> int:
    return sum(len(set(answer
                       for person in group
                       for answer in person))
                   for group in get_answers())

def count_common_answers_per_group() -> int:
    return sum(len(set.intersection(*(set(answer for answer in person)
                                      for person in group)))
               for group in get_answers())


if __name__ == "__main__":
    # part 1
    print(count_unique_answers_per_group())
    # part 2
    print(count_common_answers_per_group())
