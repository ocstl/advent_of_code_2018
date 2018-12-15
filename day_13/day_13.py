#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools

LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)


class Cart:
    def __init__(self, position, direction, track, carts):
        self.position = position
        self.direction = direction
        self.track = track
        self.carts = carts
        self.crashed = False
        # Turn left, then goes straight, then turns right. Rinse and repeat.
        self.next_turn = itertools.cycle(['left', 'straight', 'right'])

    def move(self):
        if not self.crashed:
            self.position = tuple(a + b for a, b in zip(self.position, self.direction))
            self.update_direction()
            self.check_crash()

    def update_direction(self):
        current_track = self.track[self.position[0]][self.position[1]]
        if current_track in ('|', '-'):
            pass
        elif current_track == '/':
            if self.direction == LEFT:
                self.direction = DOWN
            elif self.direction == RIGHT:
                self.direction = UP
            elif self.direction == UP:
                self.direction = RIGHT
            else:   # Going down
                self.direction = LEFT
        elif current_track == '\\':
            if self.direction == LEFT:
                self.direction = UP
            elif self.direction == RIGHT:
                self.direction = DOWN
            elif self.direction == UP:
                self.direction = LEFT
            else:   # Going down
                self.direction = RIGHT
        else:   # Intersection
            turn = next(self.next_turn)
            if turn == 'straight':
                pass
            elif turn == 'left':
                if self.direction == LEFT:
                    self.direction = DOWN
                elif self.direction == RIGHT:
                    self.direction = UP
                elif self.direction == UP:
                    self.direction = LEFT
                else:   # Going down
                    self.direction = RIGHT
            else:   # Turn right
                if self.direction == LEFT:
                    self.direction = UP
                elif self.direction == RIGHT:
                    self.direction = DOWN
                elif self.direction == UP:
                    self.direction = RIGHT
                else:   # Going down
                    self.direction = LEFT

    def check_crash(self):
        if sum(cart.position == self.position for cart in self.carts) > 1:
            for cart in self.carts:
                if cart.position == self.position:
                    cart.crashed = True


def read_problem_data(fname):
    track = list()
    carts = list()
    with open(fname, "r") as f:
        for y, line in enumerate(f):
            new_line = list()
            for x, c in enumerate(line):
                if c == '<':
                    carts.append(Cart((y, x), LEFT, track, carts))
                    new_line.append('-')
                elif c == '>':
                    carts.append(Cart((y, x), RIGHT, track, carts))
                    new_line.append('-')
                elif c == '^':
                    carts.append(Cart((y, x), UP, track, carts))
                    new_line.append('|')
                elif c == 'v':
                    carts.append(Cart((y, x), DOWN, track, carts))
                    new_line.append('|')
                else:
                    new_line.append(c)

            track.append(new_line)

    return track, carts


def first_problem(carts):
    while True:
        carts = sorted(carts, key=lambda c: c.position)
        for cart in carts:
            cart.move()
            if cart.crashed:
                return cart.position


def second_problem(carts):
    while sum(not cart.crashed for cart in carts) > 1:
        carts = (cart for cart in carts if not cart.crashed)
        carts = sorted(carts, key=lambda c: c.position)
        for cart in carts:
            cart.move()
            if cart.crashed:
                crash_position = cart.position
                # Move crashed carts out of the tracks (can't modify the list directly).
                for f in carts:
                    if f.position == crash_position:
                        f.position = (-1, -1)

    cart = [cart for cart in carts if not cart.crashed][0]
    return cart.position


def main(_args):
    track, carts = read_problem_data("day_13.txt")

    # First answer.
    first_answer = first_problem(carts)[::-1]
    print("The first answer is: {}".format(first_answer))

    # Second answer. Reset everything.
    track, carts = read_problem_data("day_13.txt")
    second_answer = second_problem(carts)[::-1]
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
