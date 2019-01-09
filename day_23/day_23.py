#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Nanobot:
    def __init__(self, x, y, z, radius):
        self.x, self.y, self.z, self.radius = x, y, z, radius

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def in_range(self, other):
        return self.distance(other) <= self.radius

    def overlapping_ranges(self, other):
        return self.distance(other) <= self.radius + other.radius


def read_problem_data(filename):
    nanobots = list()
    for line in open(filename).readlines():
        x, y, z, r = (int(x) for x in re.findall('-?\d*', line) if x)
        nanobots.append(Nanobot(x, y, z, r))

    return nanobots


def first_problem(nanobots):
    strongest_nanobot = max(nanobots, key=lambda nanobot: nanobot.radius)
    return sum(strongest_nanobot.in_range(nanobot) for nanobot in nanobots)


# Bron-Kerbosch algorithm to find maximal cliques (https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm), using
# a pivot.
def bron_kerbosch(R, P, X, connections):
    if not P and not X:
        return [R]

    possible_sets = list()
    _, pivot_vertex, neighbors = max((connections[k], k, connections[k]) for k in P.union(X))
    P_less = P.difference(neighbors)
    for v in P_less:
        results = bron_kerbosch(R.union({v}),
                                P.intersection(connections[v]),
                                X.intersection(connections[v]),
                                connections)

        possible_sets.extend(results)

    return possible_sets


def second_problem(nanobots):
    # Find connected nanobots.
    connections = dict()
    for i, nanobot in enumerate(nanobots):
        connections[i] = set(j for j, other in enumerate(nanobots) if nanobot.overlapping_ranges(other) if j != i)

    # Generate possible cliques, then grab the largest one.
    possible_cliques = bron_kerbosch(set(), set(connections.keys()), set(), connections)
    maximum_clique = max((x for x in possible_cliques), key=len)

    # Find the smallest distance that reaches within all nanobots' range. This makes a simplifying assumption that I
    # have little confidence is true in the general case.
    in_range = [nanobots[x] for x in maximum_clique]
    point = Nanobot(0, 0, 0, 0)
    step = 1000000
    while step >= 1:
        if sum(nanobot.overlapping_ranges(point) for nanobot in in_range) < len(in_range):
            point.radius += step
        else:
            point.radius -= step
            step = step // 10

    return point.radius + 1


def main(_args):
    nanobots = read_problem_data("day_23.txt")

    first_answer = first_problem(nanobots)
    print("The first answer is: {}".format(first_answer))

    second_answer = second_problem(nanobots)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
