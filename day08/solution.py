import re
from typing import Tuple, Set, List
from enum import Enum, auto


CommandType = Tuple[str, int]


COMMANDS_FUNCTIONS = {
    "nop": lambda acc, arg, index: (acc, index + 1),
    "jmp": lambda acc, arg, index: (acc, index + arg),
    "acc": lambda acc, arg, index: (acc + arg, index + 1),
}


class ExitCode(Enum):
    LOOP = auto()
    END = auto()


def _parse_line(line: str) -> CommandType:
    operation, argument = re.match(r"(\w{3}) (.*)$", line).groups()
    return operation, int(argument)


def get_parsed_lines() -> List[CommandType]:
    with open("input.txt") as f:
        return list(map(_parse_line, f.readlines()))


def calculate_accumulator(commands) -> Tuple[int, ExitCode]:
    finished_commands: Set[int] = set()
    i = 0
    acc = 0
    while True:
        finished_commands.add(i)
        command, argument = commands[i]
        acc, i = COMMANDS_FUNCTIONS[command](acc, argument, i)

        # Exit conditions
        if i in finished_commands:
            exit_code = ExitCode.LOOP
            break
        if i >= len(commands):
            exit_code = ExitCode.END
            break
    return acc, exit_code


def calculate_accumulator_fixing_commands(commands) -> int:
    for i, (command, argument) in enumerate(commands):
        if command == "jmp":
            new_command = "nop"
        elif command == "nop":
            new_command = "jmp"
        else:
            continue

        new_commands = commands.copy()
        new_commands[i] = (new_command, argument)
        acc, exit_code = calculate_accumulator(new_commands)
        if exit_code is ExitCode.END:
            return acc
    raise ValueError("Commands are not fixable")


def main():
    commands = get_parsed_lines()
    # part 1
    print(calculate_accumulator(commands)[0])
    # part 2
    print(calculate_accumulator_fixing_commands(commands))


if __name__ == "__main__":
    main()
