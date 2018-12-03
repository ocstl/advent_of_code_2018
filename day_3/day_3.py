#!/usr/bin/env python
# -*- coding: utf-8 -*-


import collections
import itertools
import re


class Claim:
    def __init__(self, string):
        self.id, self.left_edge, self.top_edge, self.width, self.height = \
            [int(x) for x in re.findall('\d*', string) if x]

    def get_surface(self):
        return itertools.product(range(self.left_edge, self.left_edge + self.width),
                                 range(self.top_edge, self.top_edge + self.height))


class Fabric:
    def __init__(self):
        self.surface = collections.defaultdict(int)

    def add_claim(self, claim: Claim):
        for point in claim.get_surface():
            self.surface[point] += 1

    def get_surface(self):
        return self.surface


def main(args):
    fabric = Fabric()

    claims = [Claim(x) for x in open("day_3.txt", "r").read().splitlines()]
    for claim in claims:
        fabric.add_claim(claim)

    # Count the points with more than two claims.
    first_answer = sum(v >= 2 for v in fabric.get_surface().values())
    print("The first answer is: {}".format(first_answer))

    # Iterate until we find the first claim whose surface is entirely composed of one claim on the fabric. We assume
    # the claims are sorted.
    second_answer = next(itertools.dropwhile(
        lambda claim: any(fabric.surface[point] > 1 for point in claim.get_surface()), claims)).id
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
