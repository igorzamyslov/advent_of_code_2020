import enum
import re
import operator
from functools import reduce
from typing import List, Dict


validators = {
    "byr": r"[12][90]([2-9][0-9]|0[12])",
    "iyr": r"20(1[0-9]|20)",
    "eyr": r"20(2[0-9]|30)",
    "hgt": r"(1([5-8][0-9]|9[0-3])cm|(59|6[0-9]|7[0-6])in)",
    "hcl": r"#[a-f0-9]{6}",
    "ecl": r"(amb|blu|brn|gry|grn|hzl|oth)",
    "pid": r"\d{9}",
}


def get_passports() -> List[Dict[str, str]]:
    with open("input.txt") as f:
        return [dict(re.findall(r"(.{3}):(.+?)(?:\s|$)", passport_string))
                for passport_string in f.read().split("\n\n")]


def passport_is_valid(passport, validate_values: bool) -> bool:
    if set(validators.keys()).issubset(set(passport.keys())):
        if not validate_values:
            return True
    else:
        return False

    return all(re.match(validator, passport[key]) 
               for key, validator in validators.items())


def find_answer(validate_values) -> int:
    return sum(1 for passport in get_passports() 
               if passport_is_valid(passport, validate_values))


if __name__ == "__main__":
    # part 1
    print(find_answer(validate_values=False))
    # part 2
    print(find_answer(validate_values=True))
