#!/usr/bin/env python
# -*- coding: utf-8 -*-


class FixedPoint:
    def __init__(self, line):
        self.position = tuple(map(int, line.strip().split(',')))

    def manhattan_distance(self, other):
        return sum(abs(x-y) for x, y in zip(self.position, other.position))


class Constellation:
    def __init__(self):
        self.points = set()

    def form_constellation(self, points):
        candidates = set()
        candidates.add(points.pop())
        while candidates:
            new_point = candidates.pop()
            self.points.add(new_point)
            candidates.update(point for point in points
                              if point not in self.points and new_point.manhattan_distance(point) <= 3)
            points.difference_update(candidates)

        points.difference_update(self.points)


def main(_args):
    points = set()
    for line in open("day_25.txt").readlines():
        points.add(FixedPoint(line))

    constellations = list()
    while points:
        new_constellation = Constellation()
        new_constellation.form_constellation(points)
        constellations.append(new_constellation)

    first_answer = len(constellations)
    print("The first answer is: {}".format(first_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
