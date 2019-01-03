#!/usr/bin/env python
# -*- coding: utf-8 -*-


def generate_map(facility_map, initial_position=0):
    # Using a stack seems to work, but this is not a general solution.
    directions = dict(zip('NSEW', [-1j, 1j, 1, -1]))
    positions = list()
    facility = {initial_position: 0}
    current_position = initial_position
    distance = 0

    for c in facility_map:
        if c in 'NSEW':
            distance += 1
            current_position += directions[c]
            if current_position in facility:
                facility[current_position] = min(facility[current_position], distance)
            else:
                facility[current_position] = distance

        elif c == '(':
            positions.append((current_position, distance))

        elif c == '|':
            current_position, distance = positions[-1]

        elif c == ')':
            current_position, distance = positions.pop()

    return facility


def main(_args):
    facility_map = generate_map(open("day_20.txt", "r").read()[1:-1])

    # Shortest path to the farthest room.
    first_answer = max(facility_map.values())
    print("The first answer is: {}".format(first_answer))

    # Number of rooms that are at least 1000 doors away.
    second_answer = sum(x >= 1000 for x in facility_map.values())
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
