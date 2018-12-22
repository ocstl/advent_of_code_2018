#!/usr/bin/env python
# -*- coding: utf-8 -*-
import queue


# Directions, in lexicographical order: up, left, right, down.
directions = (-1, 0), (0, -1), (0, 1), (1, 0)


class Unit:
    def __init__(self, position, species, cavern, hp=200, power=3):
        self.position, self.species, self.cavern, self.hp, self.power = position, species, cavern, hp, power
        self.enemy = {'E': 'G', 'G': 'E'}[species]

    @staticmethod
    def update_position(position, direction):
        return tuple(a + b for a, b in zip(position, direction))

    def move(self):
        if self.adjacent_enemy():
            return None

        # Breadth first search.
        to_do = queue.Queue()
        explored = set()
        parents = {self.position: None}
        distance = {self.position: 0}
        adjacent_enemies = list()

        to_do.put(self.position)
        while not to_do.empty():
            current_position = to_do.get()

            for direction in directions:
                new_position = self.update_position(current_position, direction)
                if new_position not in explored and new_position in self.cavern:
                    spot = self.cavern[new_position]
                    if spot is None:
                        # Stop adding squares to explore once we have found the first, as the is the minimal distance.
                        if new_position not in list(to_do.queue) and not adjacent_enemies:
                            to_do.put(new_position)
                            parents[new_position] = current_position
                            distance[new_position] = distance[current_position] + 1
                    elif spot.species == self.enemy:
                        adjacent_enemies.append(current_position)

            explored.add(current_position)

        if not adjacent_enemies:
            return None

        shortest_distance = min(distance[enemy] for enemy in adjacent_enemies)
        target_position = min(enemy for enemy in adjacent_enemies if distance[enemy] == shortest_distance)

        # Rewind the path.
        while target_position in parents:
            if parents[target_position] == self.position:
                return target_position
            else:
                target_position = parents[target_position]

    def adjacent_enemy(self):
        possible_enemies = list()
        for direction in directions:
            new_position = self.update_position(self.position, direction)
            if new_position in self.cavern\
                    and self.cavern[new_position] is not None\
                    and self.cavern[new_position].species == self.enemy:
                enemy = self.cavern[new_position]
                possible_enemies.append(enemy)

        if possible_enemies:
            return min(possible_enemies, key=lambda x: x.hp)

        return None


class BeverageBandits:
    def __init__(self, filename, elf_power=3, goblin_power=3):
        self.cavern = dict()
        self.units = list()
        self.round = 0

        with open(filename, "r") as f:
            for y, line in enumerate(f):
                for x, spot in enumerate(line):
                    if spot == '.':
                        self.cavern[(y, x)] = None
                    elif spot == 'E':
                        unit = Unit((y, x), spot, self.cavern, power=elf_power)
                        self.cavern[(y, x)] = unit
                        self.units.append(unit)
                    elif spot == 'G':
                        unit = Unit((y, x), spot, self.cavern, power=goblin_power)
                        self.cavern[(y, x)] = unit
                        self.units.append(unit)

    def round_order(self):
        reading_order = queue.Queue()
        self.units.sort(key=lambda x: x.position)

        for unit in self.units:
            reading_order.put(unit)

        return reading_order

    def new_round(self):
        ordered_units = self.round_order()
        while not ordered_units.empty():
            unit = ordered_units.get()

            if ordered_units.empty():
                self.round += 1

            if unit.hp <= 0:
                continue

            new_position = unit.move()
            if new_position:
                self.cavern[new_position] = unit
                self.cavern[unit.position] = None
                unit.position = new_position

            adjacent_enemy = unit.adjacent_enemy()
            if adjacent_enemy:
                adjacent_enemy.hp -= unit.power
                if adjacent_enemy.hp <= 0:
                    self.cavern[adjacent_enemy.position] = None
                    self.units.remove(adjacent_enemy)

            # Check whether there are any enemies left. Return True if the battle is over.
            if not any(unit.species == 'G' for unit in self.units)\
                    or not any(unit.species == 'E' for unit in self.units):
                return True

        # Return False if the battle is not over (at least one elf or goblin).
        return False

    def to_the_end(self):
        while not self.new_round():
            pass

        return self.get_outcome()

    def get_outcome(self):
        return self.round * sum(unit.hp for unit in self.units)


def second_problem(filename):
    elf_power = 4
    battle = BeverageBandits(filename, elf_power=elf_power)
    number_of_elves = sum(unit.species == 'E' for unit in battle.units)

    outcome = battle.to_the_end()
    while sum(unit.species == 'E' for unit in battle.units) < number_of_elves:
        elf_power += 1
        battle = BeverageBandits(filename, elf_power=elf_power)
        outcome = battle.to_the_end()

    return outcome


def main(_args):
    battle = BeverageBandits("day_15.txt")

    first_answer = battle.to_the_end()
    print("The first answer is: {}".format(first_answer))

    second_answer = second_problem("day_15.txt")
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
