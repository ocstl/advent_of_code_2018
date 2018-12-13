#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import itertools


class PlantRow:
    def __init__(self, state, rules):
        self.state = collections.deque(state)
        self.rules = collections.defaultdict(lambda: '.')
        self.rules.update(rules)
        self.offset = 0

    def iterate(self):
        new_state = []
        # Assume keys have a length of 5.
        key = collections.deque('.....', 5)
        self.state.extend('.....')
        self.offset -= 2

        while self.state:
            key.append(self.state.popleft())
            value = self.rules[''.join(key)]

            # Only add a dot if we already added at least one plant (to limit the growth of the string).
            if value == '#' or new_state:
                new_state.append(value)
            else:
                self.offset += 1

        # Clean up the new deque.
        while new_state.pop() == '.':
            pass

        new_state.append('#')
        self.state = collections.deque(new_state)

    def get_state(self):
        return tuple(zip(itertools.count(start=self.offset), self.state))

    def get_number_of_plants(self):
        return self.state.count('#')


def read_problem_data(fname):
    initial_state = ""
    rules = dict()
    with open(fname, "r") as f:
        for line in f:
            if "initial state" in line:
                initial_state = ''.join(x for x in line if x in ('.', '#'))
            elif "=>" in line:
                a, b = line.split("=>")
                # Don't need the other ones, we use a default dictionary.
                if b.strip() == '#':
                    rules[a.strip()] = b.strip()

    return initial_state, rules


def main(_args):
    initial_state, rules = read_problem_data("day_12.txt")
    row = PlantRow(initial_state, rules)

    # Given by the problem (20 generations).
    for x in range(20):
        row.iterate()

    first_answer = sum(idx for idx, v in row.get_state() if v == '#')
    print("The first answer is: {}".format(first_answer))

    # Given by the problem: 50 000 000 000 generations. Gliders eventually appear, so we can stop early. Alternatively,
    # pattern detection might allow an even earlier exit.
    for x in range(20, 1000):
        row.iterate()

    last_value = sum(idx for idx, v in row.get_state() if v == '#')
    row.iterate()
    new_value = sum(idx for idx, v in row.get_state() if v == '#')

    second_answer = (50000000000 - 1001) * (new_value - last_value) + new_value
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
