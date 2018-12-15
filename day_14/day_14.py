#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_new_recipe(recipes, elves):
    new_recipe = sum(recipes[elf] for elf in elves)
    if new_recipe >= 10:
        recipes.extend(divmod(new_recipe, 10))
    else:
        recipes.append(new_recipe)

    elves = [(elf + recipes[elf] + 1) % len(recipes) for elf in elves]

    return recipes, elves


def main(_args):
    recipes = [3, 7]
    elves = [0, 1]

    # First problem input. Find the next ten values after a number of iterations.
    test_string = '681901'
    tested_recipes = int(test_string)

    while len(recipes) < 10 + tested_recipes:
        recipes, elves = get_new_recipe(recipes, elves)

    print(''.join(str(x) for x in recipes[tested_recipes:tested_recipes+10]))

    # Second problem input. Find the number of recipes tested before reaching the input.
    len_test = len(test_string) + 1
    while test_string not in ''.join(str(x) for x in recipes[-len_test::]):
        recipes, elves = get_new_recipe(recipes, elves)

    print(''.join(str(x) for x in recipes).index(test_string))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
