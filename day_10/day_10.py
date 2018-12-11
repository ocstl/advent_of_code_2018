#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Point:
    def __init__(self, position, velocity):
        self.position, self.velocity = position, velocity

    def get_position_at(self, time):
        return tuple(a + time * b for a, b in zip(self.position, self.velocity))


class Sky:
    def __init__(self):
        self.points = list()

    def add_point(self, position, velocity):
        self.points.append(Point(position, velocity))

    def generate_sky_at(self, time):
        xs, ys = zip(*(point.get_position_at(time) for point in self.points))

        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)

        sky = [['.']*(max_x - min_x + 1) for _ in range(min_y, max_y + 1)]
        for point in self.points:
            x, y = point.get_position_at(time)
            sky[y-min_y][x-min_x] = '#'

        for row in sky:
            print(''.join(row))

    def get_size(self, time):
        xs, ys = zip(*(point.get_position_at(time) for point in self.points))
        return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)


def main(_args):
    sky = Sky()
    with open("day_10.txt", "r") as f:
        for line in f.readlines():
            data = tuple(map(int, (x for x in re.findall(r'-?\d*', line) if x)))
            sky.add_point(data[0:2], data[2:])

    # Iterate until the smallest surface.
    time = 0
    surface = sky.get_size(time)
    while sky.get_size(time) > sky.get_size(time + 1):
        time += 1

    # First answer.
    print("The first answer is:")
    sky.generate_sky_at(time)

    # Second answer
    print("The second answer is: {}".format(time))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
