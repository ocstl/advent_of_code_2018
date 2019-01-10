#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Group:
    def __init__(self, number, hp, immunities, weaknesses, attack_power, attack_type, initiative):
        self.number, self.hp, self.immunities, self.weaknesses, self.attack_power, self.attack_type, self.initiative = \
            number, hp, immunities, weaknesses, attack_power, attack_type, initiative

    def get_effective_power(self):
        return self.number * self.attack_power

    # Deal no damage to immune groups, double damage to weak groups.
    def deal_damage(self, other):
        if self.attack_type in other.immunities:
            return 0
        elif self.attack_type in other.weaknesses:
            return 2 * self.get_effective_power()
        else:
            return self.get_effective_power()

    def receive_damage(self, damage):
        self.number = max(0, self.number - damage // self.hp)


def create_group(line):
    number, hp, attack_power, initiative = (map(int, (x for x in re.findall('\d*', line) if x)))
    attack_type = re.search('[a-zA-Z]*(?= damage)', line).group()
    immunities = set()
    weaknesses = set()

    if "immune to" in line:
        immunities = set(x.strip() for x in re.search('(?<=immune to ).*?[a-zA-Z]*(?=[;)])', line).group().split(','))

    if "weak to" in line:
        weaknesses = set(x.strip() for x in re.search('(?<=weak to ).*?[a-zA-Z]*(?=[;)])', line).group().split(','))

    return Group(number, hp, immunities, weaknesses, attack_power, attack_type, initiative)


def read_problem_data(filename):
    immune_system = list()
    infection = list()

    current = None
    for line in open(filename).readlines():
        if "Immune System:" in line:
            current = immune_system
        elif "Infection:" in line:
            current = infection
        elif "unit" in line:
            current.append(create_group(line))

    return immune_system, infection


def battle(immune_system, infection):
    def target_selection(army, enemies):
        army.sort(key=lambda group: (-group.get_effective_power(), -group.initiative))
        targets = dict()

        for group in army:
            if len(targets) < len(enemies):
                targets[group] = max((enemy for enemy in enemies if enemy not in targets.values()),
                                     key=lambda e: (group.deal_damage(e), e.get_effective_power(), e.initiative))
                # Unselect if the group can't deal any damage.
                if group.deal_damage(targets[group]) == 0:
                    targets[group] = None
            else:
                targets[group] = None

        return targets

    def attack_phase(targets):
        attack_order = sorted(targets.items(), key=lambda x: -x[0].initiative)
        for attacker, defender in attack_order:
            if defender:
                defender.receive_damage(attacker.deal_damage(defender))

    while immune_system and infection:
        # Selection phase.
        targets = target_selection(immune_system, infection)
        targets.update(target_selection(infection, immune_system))

        # Attack phase.
        attack_phase(targets)

        # Eliminate dead groups.
        immune_system = [group for group in immune_system if group.number > 0]
        infection = [group for group in infection if group.number > 0]


def main(_args):
    immune_system, infection = read_problem_data("day_24.txt")
    battle(immune_system, infection)

    # Since only one group remains, we can sum over both.
    first_answer = sum(group.number for group in immune_system + infection)
    print("The first answer is: {}".format(first_answer))

    # Feed the reindeer some milk and cookies until its immune system is strong enough.
    '''
    boost = 0
    while not sum(group.number for group in immune_system) > 0:
        print(sum(group.number for group in immune_system))
        boost += 1
        print(boost)
        immune_system, infection = read_problem_data("day_24.txt")
        for group in immune_system:
            group.attack_power += boost

        battle(immune_system, infection)
    '''

    # Ends in a stalemate with 30 boost. Need to add a way to stop the battle.
    boost = 31
    immune_system, infection = read_problem_data("day_24.txt")
    for group in immune_system:
        group.attack_power += boost

    battle(immune_system, infection)
    second_answer = sum(group.number for group in immune_system)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
