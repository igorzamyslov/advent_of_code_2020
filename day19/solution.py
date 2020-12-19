import re

from copy import deepcopy
from typing import List, Tuple, Dict

ParsedInputType = Tuple[Dict[str, str], List[str]]


def get_parsed_input() -> ParsedInputType:
    with open("input.txt") as f:
        content = f.read()
    rules_str, messages_str = content.split("\n\n")
    return (dict(r.split(": ") for r in rules_str.split("\n")),
            list(filter(None, messages_str.split("\n"))))


def update_rules(rules: Dict[str, str]):
    for key, value in rules.items():
        rules[key] = f"({value})"

    # lazy solution for recursion
    # (based on the fact, that max length of input is ~100 characters)
    for key, value in rules.items():
        if key in value:
            for _ in range(100):
                rules[key] = re.sub(rf"(?<=[^\d]){key}(?=[^\d])", rules[key], value)

    for key1, value1 in rules.items():
        for key2, value2 in rules.items():
            if key1 == key2:
                continue
            rules[key2] = re.sub(rf"(?<=[^\d]){key1}(?=[^\d])", value1, value2)

    for key, value in rules.items():
        rules[key] = "^" + re.sub(r'[" ]', "", value) + "$"


def solve_part_one(parsed_input: ParsedInputType):
    rules, messages = parsed_input
    rules = deepcopy(rules)
    update_rules(rules)
    return sum(bool(re.match(rules["0"], m)) for m in messages)


def solve_part_two(parsed_input: ParsedInputType):
    rules, messages = parsed_input
    rules = deepcopy(rules)
    rules["8"] = "42 | 42 8"
    rules["11"] = "42 31 | 42 11 31"
    update_rules(rules)
    return sum(bool(re.match(rules["0"], m)) for m in messages)


def main():
    # data
    parsed_input = get_parsed_input()
    # part 1
    print(solve_part_one(parsed_input))
    # part 2
    print(solve_part_two(parsed_input))


if __name__ == "__main__":
    main()
