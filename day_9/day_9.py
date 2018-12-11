#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Marble:
    def __init__(self, value, previous_marble=None, next_marble=None):
        self.value = value
        self.previous_marble = previous_marble
        self.next_marble = next_marble

    def get_previous(self):
        return self.previous_marble

    def set_previous(self, other):
        self.previous_marble = other

    def get_next(self):
        return self.next_marble

    def set_next(self, other):
        self.next_marble = other

    def get_value(self):
        return self.value

    def insert(self, other):
        other.set_previous(self)
        other.set_next(self.get_next())
        other.get_next().set_previous(other)
        self.set_next(other)

    def remove(self):
        self.get_previous().set_next(self.get_next())
        self.get_next().set_previous(self.get_previous())
        return self.get_next()


class MarbleMania:
    def __init__(self, divisor=23, steps=7):
        self.current_marble = Marble(0)
        self.current_marble.set_next(self.current_marble)
        self.current_marble.set_previous(self.current_marble)
        self.divisor = divisor
        self.steps = steps

    def add_marble(self, marble):
        # Weird return rule.
        if marble % self.divisor == 0:
            for _ in range(self.steps):
                self.current_marble = self.current_marble.get_previous()

            to_return = marble + self.current_marble.get_value()
            self.current_marble = self.current_marble.remove()
            return to_return

        else:
            new_marble = Marble(marble)
            self.current_marble.get_next().insert(new_marble)
            self.current_marble = new_marble
            return None


def main(_args):
    with open("day_9.txt", "r") as f:
        nbr_players, last_marble = map(int, (x for x in re.findall(r'\d*', f.read()) if x))

    players = [0]*nbr_players
    marbles = MarbleMania()

    # First answer.
    for nbr in range(1, last_marble+1):
        score = marbles.add_marble(nbr)
        # Add the score (if applicable) to the proper player.
        if score:
            players[nbr % nbr_players] += score

    first_answer = max(players)
    print("The first answer is: {}".format(first_answer))

    # Go 100 times larger for the second answer.
    for nbr in range(last_marble+1, 100*last_marble+1):
        score = marbles.add_marble(nbr)
        # Add the score (if applicable) to the proper player.
        if score:
            players[nbr % nbr_players] += score

    second_answer = max(players)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
