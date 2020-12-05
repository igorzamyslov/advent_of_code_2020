import re
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
        

def get_passports_v2() -> List[Dict[str, str]]:
    """ regex-only solution """
    with open("input.txt") as f:
        regex = re.compile("(?m)(?:^(?<=\n\n)|\A)" 
                           + "".join(f"(?=(?:(.|.\n)*?{key}:(?P<{key}>.+?)\s{{1}})?)"
                                     for key in validators.keys()))
        return [m.groupdict() for m in regex.finditer(f.read())]


def passport_is_valid(passport, validate_values: bool) -> bool:
    return (set(validators.keys()).issubset(set(passport.keys()))
            and all(passport.values())
            and (not validate_values 
                 or all(re.match(validator, passport[key]) 
                        for key, validator in validators.items())))


def find_answer(validate_values) -> int:
    return sum(passport_is_valid(passport, validate_values) 
               for passport in get_passports_v2())


if __name__ == "__main__":
    # part 1
    print(find_answer(validate_values=False))
    # part 2
    print(find_answer(validate_values=True))