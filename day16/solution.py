from __future__ import annotations

import re
from typing import List, Dict, Tuple, Set
from functools import reduce
import operator


RangeType = Tuple[int, int]
NotesType = Dict[str, Tuple[RangeType, ...]]
TicketType = Tuple[int, ...]
ParsedInputType = Tuple[NotesType, TicketType, List[TicketType]]


def _parse_ticket(ticket: str) -> TicketType:
    return tuple(map(int, ticket.strip().split(",")))


def _parse_notes(notes: str) -> NotesType:
    regex = r"(?m)^(.+?): (\d+?)-(\d+?) or (\d+?)-(\d+?)$"
    output_dict = {}
    for match in re.finditer(regex, notes):
        key, *numbers = match.groups()
        parsed_numbers = tuple(map(int, numbers))
        output_dict[key] = (parsed_numbers[0:2], parsed_numbers[2:4])
    return output_dict


def get_parsed_input() -> ParsedInputType:
    with open("input.txt") as f:
        contents = f.read()
    notes_str, my_ticket_str, other_tickets_str = \
        re.split(r"(?m)\n\n^.+? tickets?:\n", contents)
    return (_parse_notes(notes_str), _parse_ticket(my_ticket_str),
            list(map(_parse_ticket, other_tickets_str.strip().split("\n"))))


def value_in_range(value: int, range_obj: RangeType) -> bool:
    min_value, max_value = range_obj
    return value >= min_value and value <= max_value


def solve_part_one(parsed_input: ParsedInputType):
    notes, _, tickets = parsed_input
    return sum(value
               for ticket in tickets
               for value in ticket
               if all(not value_in_range(value, r)
                      for ranges in notes.values()
                      for r in ranges))


def get_valid_tickets(parsed_input: ParsedInputType) -> List[TicketType]:
    notes, _, tickets = parsed_input
    return [ticket
            for ticket in tickets
            if all(any(value_in_range(value, r)
                       for ranges in notes.values()
                       for r in ranges)
                   for value in ticket)]


def solve_part_two(parsed_input: ParsedInputType):
    valid_tickets = get_valid_tickets(parsed_input)
    notes, my_ticket, _ = parsed_input
    key_to_indexes: Dict[str, Set[int]] = {}
    # define which keys can be covered by which indexes
    for key in notes:
        for i in range(len(my_ticket)):
            if all(any(value_in_range(ticket[i], r)
                       for r in notes[key])
                   for ticket in valid_tickets):
                key_to_indexes.setdefault(key, set()).add(i)

    # check that every key can be valid
    assert len(key_to_indexes) == len(notes)

    # stabilise key_to_indexes to only contain one index per key
    while not all(len(indexes) == 1 for indexes in key_to_indexes.values()):
        single_indexes = set(next(iter(indexes))
                             for indexes in key_to_indexes.values()
                             if len(indexes) == 1)
        for key, indexes in key_to_indexes.items():
            if len(indexes) > 1:
                key_to_indexes[key] = indexes - single_indexes

    # calculate required value
    return reduce(operator.mul,
                  (my_ticket[next(iter(indexes))]
                   for key, indexes in key_to_indexes.items()
                   if key.startswith("departure")))


def main():
    # data
    parsed_input = get_parsed_input()
    # part 1
    print(solve_part_one(parsed_input))
    # part 2
    print(solve_part_two(parsed_input))


if __name__ == "__main__":
    main()
