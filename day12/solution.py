from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple, Union

CommandType = Tuple[str, int]


DIRECTION_ANGLE = {
    "N": 0,
    "E": 90,
    "S": 180,
    "W": 270,
}
ANGLE_DIRECTION = {v: k for k, v in DIRECTION_ANGLE.items()}

DIRECTION_TO_VECTOR = {
    "N": ("x", 1),
    "S": ("x", -1),
    "E": ("y", 1),
    "W": ("y", -1),
}

TURN_TO_VECTOR = {
    "R": 1,
    "L": -1,
}


def get_parsed_lines() -> List[CommandType]:
    with open("input.txt") as f:
        return [(line[0], int(line[1:])) for line in f.readlines()]


class Executor:
    @staticmethod
    def _execute_command(obj: Union[Ship, Waypoint], command: CommandType):
        operator, value = command
        if operator in DIRECTION_TO_VECTOR:
            coordinate, vector = DIRECTION_TO_VECTOR[operator]
            obj.coordinates[coordinate] += value * vector
        elif operator in TURN_TO_VECTOR:
            obj.execute_turn(operator, value)
        elif operator in ["X", "Y"]:
            obj.coordinates[operator.lower()] += value
        else:
            raise ValueError(f"Unknown operator: {operator}")


class PositionAwareObject:
    def __init__(self, coordinates: Dict[str, int]) -> None:
        self.coordinates = coordinates


class DirectionAwareObject:
    def __init__(self, initial_direction: str) -> None:
        self.direction = initial_direction


class Ship(Executor, PositionAwareObject, DirectionAwareObject):
    def __init__(self, initial_direction: str = "E",
                 coordinates: Optional[Dict[str, int]] = None) -> None:
        if coordinates is None:
            coordinates = {"x": 0, "y": 0}
        PositionAwareObject.__init__(self, coordinates)
        DirectionAwareObject.__init__(self, initial_direction)

    def execute_turn(self, turn: str, angle: int):
        init_angle = DIRECTION_ANGLE[self.direction]
        new_angle = (init_angle + TURN_TO_VECTOR[turn]*angle) % 360
        self.direction = ANGLE_DIRECTION[new_angle]

    def execute_command(self, command: CommandType):
        try:
            super()._execute_command(self, command)
        except ValueError as exception:
            operator, value = command
            if operator == "F":
                coordinate, vector = DIRECTION_TO_VECTOR[self.direction]
                self.coordinates[coordinate] += value * vector
            else:
                raise exception

    def get_manhattan_distance(self) -> int:
        return abs(self.coordinates["x"]) + abs(self.coordinates["y"])


class Waypoint(Executor, PositionAwareObject):
    def __init__(self, ship: Ship, coordinates: Optional[Dict[str, int]] = None) -> None:
        if coordinates is None:
            coordinates = {"x": 1, "y": 10}
        PositionAwareObject.__init__(self, coordinates)
        self.ship = ship

    def get_dx_dy(self):
        return (self.coordinates["x"] - self.ship.coordinates["x"],
                self.coordinates["y"] - self.ship.coordinates["y"])


    def execute_turn(self, turn: str, angle: int):
        dx, dy = self.get_dx_dy()
        distance = math.hypot(dx, dy)
        new_angle = math.atan2(dy, dx) + math.radians(angle) * TURN_TO_VECTOR[turn]
        self.coordinates["x"] = self.ship.coordinates["x"] + round(distance * math.cos(new_angle))
        self.coordinates["y"] = self.ship.coordinates["y"] + round(distance * math.sin(new_angle))

    def execute_command(self, command: CommandType):
        try:
            super()._execute_command(self, command)
        except ValueError as exception:
            operator, value = command
            if operator == "F":
                dx, dy = self.get_dx_dy()
                self.ship.execute_command(("X", dx * value))
                self.ship.execute_command(("Y", dy * value))
                self.execute_command(("X", dx * value))
                self.execute_command(("Y", dy * value))
            else:
                raise exception


def main():
    # data
    commands = get_parsed_lines()
    # part 1
    ship = Ship()
    for command in commands:
        ship.execute_command(command)
    print(ship.get_manhattan_distance())
    # part 2
    ship = Ship()
    waypoint = Waypoint(ship)
    for command in commands:
        waypoint.execute_command(command)
    print(ship.get_manhattan_distance())


if __name__ == "__main__":
    main()
