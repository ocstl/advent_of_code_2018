#!/usr/bin/env python
# -*- coding: utf-8 -*-


import collections
import re


class Guard:
    def __init__(self, guard_id):
        self.guard_id, self.minutes_asleep = guard_id, collections.Counter()

    def add_sleep_period(self, begin, end):
        self.minutes_asleep += collections.Counter(range(begin, end))

    def total_minutes_asleep(self):
        return sum(self.minutes_asleep.values())

    def minute_most_asleep(self):
        if len(self.minutes_asleep) > 0:
            return self.minutes_asleep.most_common(1)[0]

        return 0, 0


def fill_in_guards(filename):
    minutes_filter = re.compile(r':(\d{2})')
    guard_id_filter = re.compile(r'#(\d*)')

    # Sort the input to get the right sequence of events.
    data = sorted(open(filename, "r").readlines())

    guards = dict()

    # We're assuming that a guard starts a shift before falling asleep, and falls asleep before he wakes up. Also, that
    # tend to wake up before they fall asleep.
    for line in data:
        # New (or old) guard.
        if '#' in line:
            guard_id = guard_id_filter.search(line).group(1)
            if guard_id in guards:
                current_guard = guards[guard_id]
            else:
                current_guard = Guard(guard_id)
                guards[guard_id] = current_guard

        elif 'falls asleep' in line:
            fell_asleep = int(minutes_filter.search(line).group(1))

        elif 'wakes up' in line:
            woke_up = int(minutes_filter.search(line).group(1))
            current_guard.add_sleep_period(fell_asleep, woke_up)
            fell_asleep, woke_up = None, None

    return guards


def main(args):
    # Import problem data.
    guards = fill_in_guards("day_4.txt")

    # First answer.
    most_minutes_asleep = max(guard.total_minutes_asleep() for guard in guards.values())
    sleepiest_guard = next(guard for guard in guards.values() if guard.total_minutes_asleep() == most_minutes_asleep)

    first_answer = int(sleepiest_guard.guard_id) * sleepiest_guard.minute_most_asleep()[0]
    print("The first answer is: {}".format(first_answer))

    # Second answer.
    second_sleepiest_guard = max(guards.values(), key=lambda guard: guard.minute_most_asleep()[1])

    second_answer = int(second_sleepiest_guard.guard_id) * second_sleepiest_guard.minute_most_asleep()[0]
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
