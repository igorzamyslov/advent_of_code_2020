from typing import List, Tuple

SeatType = Tuple[int, int]


def parse_line(line: str) -> SeatType:
    substitutions = {"F": "0", "L": "0", "B": "1", "R": "1"}
    for item in substitutions.items():
        line = line.replace(*item)
    return int(line[:7], base=2), int(line[7:], base=2)


def get_seats() -> List[SeatType]:
    with open("input.txt") as f:
        return list(map(parse_line, f.readlines()))


def get_seat_id(seat: SeatType) -> int:
    row, column = seat
    return row * 8 + column


def find_missing_seat() -> int:
    seat_ids = set(map(get_seat_id, get_seats()))
    all_seats = set(range(min(seat_ids), max(seat_ids)))
    [missing_seat] = all_seats - seat_ids
    return missing_seat


if __name__ == "__main__":
    # part 1
    print(max(map(get_seat_id, get_seats())))
    # part 2
    print(find_missing_seat())
