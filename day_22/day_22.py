#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import enum
import queue
import re


# From the problem definition.
FACTOR_X = 16807
FACTOR_Y = 48271
MODULO = 20183
TIME_MOVE = 1
TIME_CHANGE_EQUIPMENT = 7


class Equipment(enum.IntEnum):
    NEITHER = 0
    TORCH = 1
    CLIMBING_GEAR = 2


class RegionType(enum.IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2


ALLOWED_EQUIPMENT = {RegionType.ROCKY: (Equipment.TORCH, Equipment.CLIMBING_GEAR),
                     RegionType.WET: (Equipment.NEITHER, Equipment.CLIMBING_GEAR),
                     RegionType.NARROW: (Equipment.NEITHER, Equipment.TORCH)}


class Region:
    def __init__(self, position, depth, cave):
        self.position, self.depth, self.cave = position, depth, cave
        self.geologic_index, self.erosion_level, self.type = None, None, None

    def get_geologic_index(self):
        if self.geologic_index is None:
            if any(x == 0 for x in self.position):
                self.geologic_index = (self.position[0] * FACTOR_X + self.position[1] * FACTOR_Y + self.depth)
            else:
                self.geologic_index = (self.cave[(self.position[0] - 1, self.position[1])].get_erosion_level() *
                                       self.cave[(self.position[0], self.position[1] - 1)].get_erosion_level() +
                                       self.depth)

        return self.geologic_index

    def get_erosion_level(self):
        if self.erosion_level is None:
            self.erosion_level = self.get_geologic_index() % MODULO

        return self.erosion_level

    def get_type(self):
        if self.type is None:
            self.type = RegionType(self.get_erosion_level() % 3)

        return self.type


class Cave(dict):
    def __init__(self, depth):
        super(Cave, self).__init__()
        self.depth = depth

    def __missing__(self, key):
        value = Region(key, self.depth, self)
        self[key] = value
        return value

    def generate(self, target):
        _ = self[target].get_type()


def read_problem_data(filename):
    depth, target = None, None
    for line in open(filename).readlines():
        if "depth" in line:
            depth = next(int(x) for x in re.findall('\d*', line) if x)
        else:
            target = tuple(int(x) for x in re.findall('\d*', line) if x)

    return depth, target


def shortest_path(cave, target, initial_position=(0, 0), initial_equipment=Equipment.TORCH):
    def get_adjacent_regions(z):
        positions = ((z.position[0] + x, z.position[1] + y) for x, y in ((-1, 0), (1, 0), (0, -1), (0, 1)))
        return (VisitedRegion(cave[pos].position, z.equipment) for pos in positions if pos[0] >= 0 and pos[1] >= 0)

    def get_alternate_equipment(z):
        return next(VisitedRegion(z.position, equ) for equ in ALLOWED_EQUIPMENT[cave[z.position].get_type()]
                    if equ is not z.equipment)

    VisitedRegion = collections.namedtuple('VisitedRegion', ['position', 'equipment'])

    visited = dict()
    to_do = queue.PriorityQueue()

    to_do.put((0, VisitedRegion(initial_position, initial_equipment)))

    while not to_do.empty():
        distance, current = to_do.get()

        # Return once we have found the shortest distance.
        if current.position == target and current.equipment is Equipment.TORCH:
            return distance

        # Check if visited already.
        if current in visited and visited[current] <= distance:
            continue
        else:
            visited[current] = distance

        # Try to move up, down, left or right.
        for adjacent in get_adjacent_regions(current):
            if adjacent.equipment in ALLOWED_EQUIPMENT[cave[adjacent.position].get_type()]:
                if adjacent not in visited or visited[adjacent] > distance + TIME_MOVE:
                    to_do.put((distance + TIME_MOVE, adjacent))
                elif distance + TIME_MOVE < visited[adjacent]:
                    to_do.put((distance + TIME_MOVE, adjacent))

        # Try changing equipment.
        alternate_equipment = get_alternate_equipment(current)
        if alternate_equipment not in visited or visited[alternate_equipment] > distance + TIME_CHANGE_EQUIPMENT:
            to_do.put((distance + TIME_CHANGE_EQUIPMENT, alternate_equipment))


def main(_args):
    depth, target = read_problem_data("day_22.txt")
    cave = Cave(depth)

    # First answer: sum of the types of the regions for the rectangle from the mouth of the cave to the target. The
    # target's region is rocky (0), no matter its geologic index.
    cave.generate(target)
    cave[target].type = 0
    first_answer = sum(region.get_type() for region in cave.values())
    print("The first answer is: {}".format(first_answer))

    # Second answer. Shortest path to the target.
    second_answer = shortest_path(cave, target)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    sys.exit(main(sys.argv))
