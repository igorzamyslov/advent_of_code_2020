import re
from typing import Tuple, Dict, Set


ContainedColoursInfoType = Dict[str, int]
ColoursInfoType = Dict[str, Dict[str, int]]


def _parse_line(line: str) -> Tuple[str, ContainedColoursInfoType]:
    colour, colour_contains_string = line.split(" bags contain ")
    contained_colours_info = {}
    for match in re.finditer(r"(\d+?) (.+?) bags?[,\.]", colour_contains_string):
        count, contained_colour = match.groups()
        contained_colours_info[contained_colour] = int(count)
    return colour, contained_colours_info


def get_parsed_lines() -> ColoursInfoType:
    with open("input.txt") as f:
        return dict(map(_parse_line, f.readlines()))


def get_containing_colours(colour: str, colours_info: ColoursInfoType) -> Set[str]:
    containing_colours = set()
    for containing_colour, contained_colours in colours_info.items():
        if colour in contained_colours:
            containing_colours.add(containing_colour)
            containing_colours.update(get_containing_colours(containing_colour, colours_info))
    return containing_colours


def count_contained_bags(colour: str, colours_info: ColoursInfoType, multiplier: int = 1) -> int:
    return sum(n * multiplier + count_contained_bags(c, colours_info, multiplier * n)
               for c, n in colours_info[colour].items())


def main():
    colour_in_question = "shiny gold"
    colours_info = get_parsed_lines()
    # part 1
    print(len(get_containing_colours(colour_in_question, colours_info)))
    # part 2
    print(count_contained_bags(colour_in_question, colours_info))


if __name__ == "__main__":
    main()
