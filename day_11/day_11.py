#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools


def power_level(x, y, serial_number):
    return ((((x + 10) * y + serial_number) * (x + 10)) // 100) % 10 - 5


def square_power(x, y, square_size, power_grid):
    return sum(power_grid[y-1][x-1] for x, y in itertools.product(range(x, x+square_size), range(y, y+square_size)))


def variable_size(x, y, grid_size, power_grid):
    power_levels = {(x, y, 0): 0}
    for size in range(1, grid_size - max(x, y) + 1):
        power_levels[(x, y, size)] = (power_levels[(x, y, size-1)] - power_grid[y-1+size][x-1+size]
                                      + sum(power_grid[y-1+size][x-1+t] for t in range(1, size+1))
                                      + sum(power_grid[y-1+t][x-1+size] for t in range(1, size+1))
                                      )

    return max((c for c in power_levels.items()), key=lambda c: c[1])


def main(_args):
    # Given in the problem definition.
    serial_number = 42
    grid_size = 300
    square_size = 3

    power_grid = tuple(tuple(power_level(x+1, y+1, serial_number) for x in range(grid_size)) for y in range(grid_size))

    power_levels = dict()
    for x in range(1, grid_size + 1 - square_size):
        for y in range(1, grid_size + 1 - square_size):
            power_levels[(x, y)] = square_power(x, y, square_size, power_grid)

    # First answer.
    first_answer = max(power_levels.keys(), key=lambda key: power_levels[key])
    print("The first answer is: {}".format(first_answer))

    # Second answer.
    power_levels = dict()
    for x in range(1, grid_size + 1):
        for y in range(1, grid_size + 1):
            k, v = variable_size(x, y, grid_size, power_grid)
            power_levels[k] = v

    # Pesky off by one. Add (1, 1) to the resulting output.
    second_answer = max(power_levels.keys(), key=lambda key: power_levels[key])
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
