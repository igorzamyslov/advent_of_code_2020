from typing import List, Dict


def get_parsed_lines() -> List[int]:
    with open("input.txt") as f:
        return list(map(int, f.readlines()))


def find_differences(adapters: List[int]) -> Dict[int, int]:
    current = adapters[0]  # ba dum tss
    differences = {1: 0, 2: 0, 3: 0}
    for adapter in adapters[1:]:
        difference = adapter - current
        assert difference in differences
        differences[difference] += 1
        current = adapter
    return differences


def get_valid_adapters(given_adapter: int, adapters: List[int]) -> List[int]:
    valid_adapters = []
    for adapter in adapters[adapters.index(given_adapter) + 1:]:
        if adapter - given_adapter > 3:
            break
        valid_adapters.append(adapter)
    return valid_adapters


def count_valid_arrangements(adapters: List[int], start_adapter: int,
                             valid_adapters_dict: Dict[int, List[int]] = None,
                             cache: Dict[int, int] = None) -> int:
    if valid_adapters_dict is None:
        valid_adapters_dict = {a: get_valid_adapters(a, adapters) for a in adapters}
    if cache is None:
        cache = {}
    valid_adapters = valid_adapters_dict[start_adapter]
    if start_adapter not in cache:
        cache[start_adapter] = sum(count_valid_arrangements(adapters, a, valid_adapters_dict, cache)
                                   for a in valid_adapters) if valid_adapters else 1
    return cache[start_adapter]


def main():
    # data
    adapters = get_parsed_lines()
    adapters.append(0)  # outlet
    adapters.append(max(adapters) + 3)  # default adapter
    adapters.sort()
    # part 1
    differences = find_differences(adapters)
    print(differences[1] * differences[3])
    # part 2
    print(count_valid_arrangements(adapters, 0))


if __name__ == "__main__":
    main()
