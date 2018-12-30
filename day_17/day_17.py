#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum
import re


State = enum.Enum('State', 'FLOWING SETTLED')


def read_problem_data(filename):
    clay_positions = set()
    for line in open(filename, "r"):
        if line.startswith('x'):
            x, y_min, y_max = (int(x) for x in re.findall('\d*', line) if x)
            for y in range(y_min, y_max+1):
                clay_positions.add((x, y))

        elif line.startswith('y'):
            y, x_min, x_max = (int(x) for x in re.findall('\d*', line) if x)
            for x in range(x_min, x_max+1):
                clay_positions.add((x, y))

    return clay_positions


def flow(spring_position, clay_positions):
    to_do = list()
    watered = dict()
    max_depth = max(y for x, y in clay_positions)

    def check_left(loc):
        positions = list()
        left = loc[0] - 1, loc[1]
        positions.append(left)

        if left in clay_positions:
            return True, []

        down = left[0], left[1] + 1
        if down in clay_positions or (down in watered and watered[down] is State.SETTLED):
            clay, locs = check_left(left)
            return clay, positions + locs

        # All that is left is that the water is flowing in the down direction, or there is nothing there.
        return False, positions

    def check_right(loc):
        positions = list()
        right = loc[0] + 1, loc[1]
        positions.append(right)

        if right in clay_positions:
            return True, []

        down = right[0], right[1] + 1
        if down in clay_positions or (down in watered and watered[down] is State.SETTLED):
            clay, locs = check_right(right)
            return clay, positions + locs

        # All that is left is that the water is flowing in the down direction, or there is nothing there.
        return False, positions

    to_do.append(spring_position)
    while to_do:
        position = to_do.pop()
        down = position[0], position[1] + 1
        if position[1] > max_depth:
            continue

        # If the water cannot flow down, flow left and right.
        elif down in clay_positions or (down in watered and watered[down] is State.SETTLED):
            blocked_left, left_positions = check_left(position)
            blocked_right, right_positions = check_right(position)

            # If the water settles, go back one step.
            if blocked_left and blocked_right:
                flow_state = State.SETTLED
                to_do.append((position[0], position[1] - 1))
            else:
                flow_state = State.FLOWING

            watered[position] = flow_state
            for pos in left_positions + right_positions:
                watered[pos] = flow_state

            # Add the flowing water to the to do list.
            if not blocked_left:
                leftmost = min(left_positions)
                to_do.append((leftmost[0], leftmost[1] + 1))
            if not blocked_right:
                rightmost = max(right_positions)
                to_do.append((rightmost[0], rightmost[1] + 1))

            continue

        # If the water is flowing, nothing to do.
        elif down in watered and watered[down] is State.FLOWING:
            watered[position] = State.FLOWING
            continue

        else:
            watered[position] = State.FLOWING
            to_do.append(down)

    return watered


def main(_args):
    clay_positions = read_problem_data("day_17.txt")
    watered = flow((500, 0), clay_positions)

    # First answer.
    min_y = min(y for x, y in clay_positions)
    max_y = max(y for x, y in clay_positions)
    first_answer = sum(1 for x, y in watered if min_y <= y <= max_y)
    print("The first answer is: {}".format(first_answer))

    # Second answer (settled water).
    second_answer = sum(1 for x, y in watered if min_y <= y <= max_y and watered[x, y] is State.SETTLED)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(5000)
    sys.exit(main(sys.argv))
