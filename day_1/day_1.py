#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools


def main(args):
    frequency_list = list(map(int, open("day_1.txt", "r").read().split()))

    # First problem is a simple sum.
    print("The first answer is: {}".format(sum(frequency_list)))

    # Need to keep track of visited frequencies for the second problem.
    visited_frequencies = set()
    current_frequency = 0
    frequency_cycle = itertools.cycle(frequency_list)

    while current_frequency not in visited_frequencies:
        visited_frequencies.add(current_frequency)
        current_frequency += next(frequency_cycle)

    print("The second answer is: {}".format(current_frequency))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
