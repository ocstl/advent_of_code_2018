#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re


def reduce_polymer(polymer):
    resulting_polymer = []
    for c in polymer:
        if not resulting_polymer:
            resulting_polymer.append(c)
        elif resulting_polymer[-1] == c.swapcase():
            resulting_polymer.pop()
        else:
            resulting_polymer.append(c)

    return resulting_polymer


def remove_one_type(polymer):
    unit_types = set(polymer.lower())
    return min(len(reduce_polymer(re.sub(unit_type, "", polymer, flags=re.I))) for unit_type in unit_types)


def main(_args):
    polymer = open("day_5.txt", "r").read()

    first_answer = len(reduce_polymer(polymer))
    print("The first answer is: {}".format(first_answer))

    second_answer = remove_one_type(polymer)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
