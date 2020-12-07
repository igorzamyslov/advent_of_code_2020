import re
from typing import List, Tuple, Dict, Set


ContainedColourInfoType = Tuple[str, int]
ColoursInfoType = Dict[str, List[ContainedColourInfoType]]


def _parse_line(line: str) -> Tuple[str, List[ContainedColourInfoType]]:
    colour, colour_contains_string = line.split(" bags contain ")
    colour_contains_list = []
    for match in re.finditer(r"(\d+?) (.+?) bags?[,\.]", colour_contains_string):
        count, contained_colour = match.groups()
        colour_contains_list.append((contained_colour, int(count)))
    return colour, colour_contains_list


def get_parsed_lines() -> ColoursInfoType:
    with open("input.txt") as f:
        return dict(map(_parse_line, f.readlines()))


def get_containing_colours(colour: str, colours_info: ColoursInfoType) -> Set[str]:
    containing_colours = set()
    for containing_colour, contained_colours in colours_info.items():
        if any(contained_colour == colour for contained_colour, _ in contained_colours):
            containing_colours.add(containing_colour)
            containing_colours.update(get_containing_colours(containing_colour, colours_info))
    return containing_colours


def count_contained_bags(colour: str, colours_info: ColoursInfoType, multiplier: int = 1) -> int:
    return sum(count * multiplier + count_contained_bags(c_colour, colours_info,
                                                         multiplier * count)
               for c_colour, count in colours_info[colour])


def main():
    colour_in_question = "shiny gold"
    colours_info = get_parsed_lines()
    # part 1
    print(len(get_containing_colours(colour_in_question, colours_info)))
    # part 2
    print(count_contained_bags(colour_in_question, colours_info))


if __name__ == "__main__":
    main()
