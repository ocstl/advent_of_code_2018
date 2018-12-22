#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import re


class Device:
    def __init__(self, registers=[0]*4):
        self._registers = registers
        self.opcodes = {
            0: self.addr,
            1: self.addi,
            2: self.mulr,
            3: self.muli,
            4: self.banr,
            5: self.bani,
            6: self.borr,
            7: self.bori,
            8: self.setr,
            9: self.seti,
            10: self.gtir,
            11: self.gtri,
            12: self.gtrr,
            13: self.eqir,
            14: self.eqri,
            15: self.eqrr,
        }

    def execute(self, instruction):
        self.opcodes[instruction[0]](*instruction[1:])

    def get_registers(self):
        return self._registers

    def remap_opcodes(self, new_mapping):
        new_opcodes = dict()
        for k, v in new_mapping.items():
            new_opcodes[k] = self.opcodes[v]

        self.opcodes = new_opcodes

    def addr(self, a, b, c):
        self._registers[c] = self._registers[a] + self._registers[b]

    def addi(self, a, b, c):
        self._registers[c] = self._registers[a] + b

    def mulr(self, a, b, c):
        self._registers[c] = self._registers[a] * self._registers[b]

    def muli(self, a, b, c):
        self._registers[c] = self._registers[a] * b

    def banr(self, a, b, c):
        self._registers[c] = self._registers[a] & self._registers[b]

    def bani(self, a, b, c):
        self._registers[c] = self._registers[a] & b

    def borr(self, a, b, c):
        self._registers[c] = self._registers[a] | self._registers[b]

    def bori(self, a, b, c):
        self._registers[c] = self._registers[a] | b

    def setr(self, a, _b, c):
        self._registers[c] = self._registers[a]

    def seti(self, a, _b, c):
        self._registers[c] = a

    def gtir(self, a, b, c):
        self._registers[c] = int(a > self._registers[b])

    def gtri(self, a, b, c):
        self._registers[c] = int(self._registers[a] > b)

    def gtrr(self, a, b, c):
        self._registers[c] = int(self._registers[a] > self._registers[b])

    def eqir(self, a, b, c):
        self._registers[c] = int(a == self._registers[b])

    def eqri(self, a, b, c):
        self._registers[c] = int(self._registers[a] == b)

    def eqrr(self, a, b, c):
        self._registers[c] = int(self._registers[a] == self._registers[b])


def read_samples(filename):
    Sample = collections.namedtuple('Sample', ('initial', 'opcode', 'instruction', 'final'))

    samples = list()
    with open(filename, "r") as f:
        for idx, line in enumerate(f):
            values = [int(x) for x in re.findall('\d*', line) if x]
            # Start a new test.
            if 'Before' in line:
                initial = values
            elif 'After' in line:
                final = values
            elif values:
                opcode, *instruction = values
            else:
                samples.append(Sample(initial, opcode, instruction, final))
                del initial, final, opcode, instruction

    return samples


def run_test(possible, sample):
    # Pass the initial state by value, not reference.
    device = Device(sample.initial.copy())
    device.execute([possible] + sample.instruction)
    return device.get_registers() == sample.final


def test_samples(samples):
    results = list()
    for sample in samples:
        results.append([possible for possible in range(16) if run_test(possible, sample)])

    return results


def get_proper_opcodes(samples, tests):
    possible_opcodes = dict()
    for x in range(16):
        possible_opcodes[x] = set(range(16))

    for sample, test in zip(samples, tests):
        possible_opcodes[sample.opcode].intersection_update(set(test))

    new_opcodes = dict()
    while possible_opcodes:
        k, v = min((k, *v) for k, v in possible_opcodes.items() if len(v) == 1)
        new_opcodes[k] = v
        del possible_opcodes[k]

        for possibilities in possible_opcodes.values():
            possibilities.discard(v)

    return new_opcodes

def run_test_program(filename, new_opcodes):
    device = Device()
    device.remap_opcodes(new_opcodes)

    with open(filename, "r") as f:
        for line in f:
            device.execute([int(x) for x in line.split()])

    return device.get_registers()

def main(_args):
    samples = read_samples("day_16_samples.txt")
    tests = test_samples(samples)

    first_answer = sum(len(v) >= 3 for v in tests)
    print("The first answer is: {}".format(first_answer))

    new_opcodes = get_proper_opcodes(samples, tests)
    final_registers = run_test_program("day_16_test_program.txt", new_opcodes)
    print("The second answer is: {}".format(final_registers[0]))


    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
