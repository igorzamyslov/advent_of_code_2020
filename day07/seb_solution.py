#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Created on 07/12/2020 07:56
@author: Sebastian
check_my_bag.py is a script for advent of code 7
"""

import os
from typing import List, Union


class Bag:
    @staticmethod
    def direct_init(amount, color, form):
        return Bag(f'{amount} {form} {color}')

    def __init__(self, line: str):
        if line == ' no other bags.':
            self.amount = 0
            self.color = None
            self.form = None
        else:
            (amount, form, color, *_) = line.strip(' ').split(' ')
            self.form = form
            self.color = color
            if amount == 'no':
                self.amount = 0
            else:
                self.amount = int(amount)

    def check_shiny_gold(self) -> bool:
        return self.check_bag(Bag.direct_init(1, 'gold', 'shiny'))

    def check_bag(self, other_Bag):
        return self.amount >= other_Bag.amount and self.color == other_Bag.color and self.form == other_Bag.form


def search_by_initial_rule_list_upwards(rule_list: List[Bag]):
    no_new_set_found = False
    waves_of_bags = set()
    while not no_new_set_found:
        pre_size = len(waves_of_bags)
        act_found_rules = set()
        for rule in rule_list:
            for outer_rule, inner_rule_list in bag_rule.items():
                if any([inner_bag.check_bag(rule) for inner_bag in inner_rule_list]):
                    act_found_rules.add(outer_rule)
        waves_of_bags.update(act_found_rules)
        if pre_size == len(waves_of_bags):
            no_new_set_found = True
        else:
            rule_list = list(act_found_rules)
    return waves_of_bags


class BagTree:
    def __init__(self, parent: Union[Bag, None], childs: List[Bag], own: Bag):
        self.parent = parent
        self.childs = childs
        self.own = own
        self.childs_tree: List[BagTree] = []

    def generate_child_trees(self, all_bag_rule):
        for bag in self.childs:
            if bag.amount == 0:
                # this should be the end of the recursion
                self.childs_tree.append(BagTree(parent=self.own, childs=[], own=bag))
                continue
            [childs_childs] = [val_list for key, val_list in all_bag_rule.items() if
                               key.color == bag.color and key.form == bag.form]
            self.childs_tree.append(BagTree(parent=self.own, childs=childs_childs, own=bag))

    def recursive_tree_fillin(self, all_bag_rule):
        if not self.childs_tree:
            self.generate_child_trees(all_bag_rule)
        for child_tree in self.childs_tree:
            child_tree.recursive_tree_fillin(all_bag_rule)

    def recursive_top_down_traversal(self):
        # not consider own bag
        resulting = 0
        for child in self.childs_tree:
            resulting += child.bag_contained()
        return resulting

    def bag_contained(self):
        if self.childs[0].amount == 0:
            return self.own.amount
        else:
            return self.own.amount + self.own.amount * sum(
                [child_tree.bag_contained() for child_tree in self.childs_tree])


def load_input_file(folder: str, file: str = 'input.txt'):
    """load the file input.txt from the given folder"""
    with open(os.path.join(folder, file), 'r') as f:
        return [e.rstrip() for e in f.readlines()]



if __name__ == "__main__":

    print("Welcome to check_my_bag.py")
    input_lines = load_input_file(os.getcwd())

    found_golden_bags = 0
    surround_bags_found = set()
    bag_rule = {}
    for line in input_lines:
        line_split = line.split('contain')
        surround_bag_split = line_split[0].split(' ')
        surround_bag = Bag.direct_init(1, surround_bag_split[1], surround_bag_split[0])
        bag_rule_list: List[Bag] = [Bag(f) for f in line_split[1].split(',')]
        bag_rule[surround_bag] = bag_rule_list

    # tree search up
    rules_to_check = [Bag.direct_init(1, 'gold', 'shiny')]
    waves_of_bags = search_by_initial_rule_list_upwards(rules_to_check)
    print(len(waves_of_bags))
    # tree search down
    [rules_to_check] = [val for key, val in bag_rule.items() if
                        key.color == 'gold' and key.form == 'shiny']
    root_tree = BagTree(None, rules_to_check, Bag.direct_init(1, 'gold', 'shiny'))
    root_tree.recursive_tree_fillin(all_bag_rule=bag_rule)
    print(root_tree.recursive_top_down_traversal())
