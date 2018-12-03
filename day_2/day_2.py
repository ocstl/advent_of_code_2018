#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import itertools


def checksum(strings):
    counters = list(collections.Counter(string) for string in strings)
    nbr_2s = sum(any(v == 2 for v in counter.values()) for counter in counters)
    nbr_3s = sum(any(v == 2 for v in counter.values()) for counter in counters)
    return nbr_2s * nbr_3s


def count_different_characters(string1, string2):
    return sum(c1 != c2 for (c1, c2) in zip(string1, string2))


def strings_with_one_difference(strings):
    comparisons = itertools.product(strings, strings)
    return next(itertools.dropwhile(lambda c: count_different_characters(c[0], c[1]) != 1, comparisons))


def main(args):
    box_ids = open("day_2.txt", "r").read().split()

    first_answer = checksum(box_ids)
    print("The first answer is {}".format(first_answer))

    # Assume there is only one match.
    similar_ids = strings_with_one_difference(box_ids)
    second_answer = ''.join(c1 for (c1, c2) in zip(similar_ids[0], similar_ids[1]) if c1 == c2)
    print("The second answer is " + second_answer)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
