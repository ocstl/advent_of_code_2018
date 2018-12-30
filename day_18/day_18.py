#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools


class Landscape:
    def __init__(self, landscape, size=50):
        self.size = size
        self.generation = 0
        self.open_ground = set()
        self.trees = set()
        self.lumberyards = set()

        for k, v in landscape.items():
            if v == '.':
                self.open_ground.add(k)
            elif v == '|':
                self.trees.add(k)
            elif v == '#':
                self.lumberyards.add(k)

    def get_number_of_trees(self):
        return len(self.trees)

    def get_number_of_lumberyards(self):
        return len(self.lumberyards)

    def get_number_of_open_ground(self):
        return len(self.open_ground)

    def get_resource_value(self):
        return self.get_number_of_trees() * self.get_number_of_lumberyards()

    def as_string(self):
        result = list(' '*self.size**2)
        for x, y in self.open_ground:
            result[y * self.size + x] = '.'

        for x, y, in self.trees:
            result[y * self.size + x] = '|'

        for x, y in self.lumberyards:
            result[y * self.size + x] = '#'

        return ''.join(result)

    def update(self):
        self.generation += 1

        new_open_ground = set()
        new_trees = set()
        new_lumberyards = set()

        # Turn open ground to trees if there are more than 3 adjacent trees. We can ignore the center point as we know
        # it is open ground.
        for position in self.open_ground:
            if sum(pos in self.trees for pos in self.adjacent_positions(position)) >= 3:
                new_trees.add(position)
            else:
                new_open_ground.add(position)

        # Turn trees into lumberyards if there are more than 3 adjacent lumberyards. We can ignore the center point as
        # we know it is a tree.
        for position in self.trees:
            if sum(pos in self.lumberyards for pos in self.adjacent_positions(position)) >= 3:
                new_lumberyards.add(position)
            else:
                new_trees.add(position)

        # Since we know the lumberyard is a lumberyard, we cannot use the center point to check if it is neighboured by
        # another lumberyard.
        for position in self.lumberyards:
            adjacents = [x for x in self.adjacent_positions(position) if x != position]
            if any(pos in self.trees for pos in adjacents) and \
                    any(pos in self.lumberyards for pos in adjacents):
                new_lumberyards.add(position)
            else:
                new_open_ground.add(position)

        self.open_ground = new_open_ground
        self.trees = new_trees
        self.lumberyards = new_lumberyards

    @staticmethod
    def adjacent_positions(position):
        return itertools.product(range(position[0]-1, position[0]+2), range(position[1]-1, position[1]+2))


def read_problem_data(filename):
    landscape = dict()
    for y, line in enumerate(open(filename, "r").read().splitlines()):
        for x, c in enumerate(line):
            landscape[x, y] = c

    return landscape


def main(_args):
    landscape = Landscape(read_problem_data("day_18.txt"))

    # Update for ten minutes.
    for _ in range(10):
        landscape.update()

    print("The first answer is: {}".format(landscape.get_resource_value()))

    # Second answer. Have to find a cycle.
    landscape = Landscape(read_problem_data("day_18.txt"))
    values = list()

    new_value = landscape.as_string()
    while new_value not in values:
        values.append(new_value)
        landscape.update()
        new_value = landscape.as_string()

    last_index = len(values)
    previous_index = values.index(new_value)
    cycle_length = last_index - previous_index

    further_iterations = (1000000000 - last_index) % cycle_length
    for _ in range(further_iterations):
        landscape.update()

    print("The second answer is: {}".format(landscape.get_resource_value()))

    return 0


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    sys.exit(main(sys.argv))
