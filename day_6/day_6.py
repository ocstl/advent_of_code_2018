#!/usr/bin/env python
# -*- coding: utf-8 -*-


import collections
import itertools


class Point:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def get_x(self):
        return self.coordinates[0]

    def get_y(self):
        return self.coordinates[1]

    def manhattan_distance(self, coordinates):
        return sum(abs(x-y) for x, y in zip(self.coordinates, coordinates))


class Map:
    def __init__(self):
        self.points = list()
        self.map = dict()

    def add_point(self, coordinates):
        # Erase the former map to make sure we have to redraw it.
        self.map.clear()
        self.points.append(Point(coordinates))

    def get_dimensions(self):
        x = [point.get_x() for point in self.points]
        y = [point.get_y() for point in self.points]

        return (min(x), min(y)), (max(x), max(y))

    def generate_map(self):
        # Do not redraw when unnecessary.
        if self.map:
            return self.map

        (min_x, min_y), (max_x, max_y) = self.get_dimensions()
        for coordinate in itertools.product(range(min_x, max_x+1), range(min_y, max_y+1)):
            distances = tuple(point.manhattan_distance(coordinate) for point in self.points)
            if distances.count(min(distances)) > 1:
                closest_point = None
            else:
                closest_point = distances.index(min(distances))

            self.map[coordinate] = closest_point

        return self.map

    def get_bordering_points(self):
        if not self.map:
            self.generate_map()

        (min_x, min_y), (max_x, max_y) = self.get_dimensions()
        return set(v for (x, y), v in self.map.items() if x in (min_x, max_x) or y in (min_y, max_y))

    def calculate_safe_region(self, max_distance):
        def test_distance(coordinate):
            # Use an accumulator to try to filter more rapidly.
            sum_distances = itertools.accumulate(point.manhattan_distance(coordinate) for point in self.points)
            try:
                while next(sum_distances) < max_distance:
                    pass
            except StopIteration as _:
                return True

            return False

        # Unlikely to find a point beyond the maximum dimensions.
        (min_x, min_y), (max_x, max_y) = self.get_dimensions()
        return sum(map(test_distance, itertools.product(range(min_x, max_x), range(min_y, max_y))))


def main(_args):
    my_map = Map()

    for line in open("day_6.txt", "r").readlines():
        point = tuple(map(int, line.split(',')))
        my_map.add_point(point)

    bordering_points = my_map.get_bordering_points()
    surfaces = collections.Counter(point for point in my_map.generate_map().values() if point not in bordering_points)

    first_answer = max(surfaces.values())
    print("The first answer is: {}".format(first_answer))

    # The maximum distance (10000) is taken from the problem definition.
    second_answer = my_map.calculate_safe_region(10000)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
