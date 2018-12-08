#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import queue


class Step:
    def __init__(self, name):
        self.name = name
        self.preceding_steps = list()
        self.following_steps = list()

    def add_following_step(self, other):
        self.following_steps.append(other)

    def add_preceding_step(self, other):
        self.preceding_steps.append(other)

    def get_preceding_steps(self):
        return "".join(step.name for step in self.preceding_steps)


def read_problem_data(fname):
    steps = dict()

    first_step = re.compile('Step ([A-Z])')
    second_step = re.compile('step ([A-Z])')

    with open(fname, "r") as f:
        for line in f.readlines():
            preceding_name = first_step.search(line).group(1)
            following_name = second_step.search(line).group(1)

            if preceding_name not in steps:
                steps[preceding_name] = Step(preceding_name)

            if following_name not in steps:
                steps[following_name] = Step(following_name)

            steps[preceding_name].add_following_step(steps[following_name])
            steps[following_name].add_preceding_step(steps[preceding_name])

    return steps


def return_order(steps):
    result = ""
    nbr_steps = len(steps.keys())

    # Check over all potential next steps for the first in alphabetical order, until we have all the steps.
    while len(result) < nbr_steps:
        result += min(step.name for step in steps.values() if all(s in result for s in step.get_preceding_steps())
                      and step.name not in result)

    return result


def time_until_finish(steps, nbr_workers=5, base_time=60):
    # The current work queue should be filled with (time_at_finished, step) tuples.
    workers = queue.PriorityQueue(maxsize=nbr_workers)
    current_work = set()
    finished_steps = set()

    time = 0
    while len(finished_steps) < len(steps):
        print("At {}, steps {} are finished. Current work: {}".format(time, finished_steps, workers.queue))
        # If all workers are busy, wait until one of them is free.
        if workers.full():
            time, done_step = workers.get()
            workers.task_done()
            finished_steps.add(done_step)
            current_work.remove(done_step)
            pass

        # Add steps that are now available to be worked on (all preceding steps are finished).
        available_steps = set(step.name for step in steps.values()
                              if all(s in finished_steps for s in step.get_preceding_steps())
                              and step.name not in finished_steps
                              and step.name not in current_work)

        # Start work on a new step if a worker is available.
        while available_steps and not workers.full():
            new_step = min(available_steps)
            available_steps.remove(new_step)
            time_to_finish = time + ord(new_step) - ord('A') + 1 + base_time
            workers.put((time_to_finish, new_step))
            current_work.add(new_step)

        # Collect newly finished steps.
        if not workers.empty():
            time, done_step = workers.get()
            workers.task_done()
            finished_steps.add(done_step)
            current_work.remove(done_step)
            pass

    return time


def main(_args):
    steps = read_problem_data("day_7.txt")
    first_answer = return_order(steps)
    print("The first answer is: " + first_answer)

    second_answer = time_until_finish(steps, nbr_workers=5, base_time=60)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
