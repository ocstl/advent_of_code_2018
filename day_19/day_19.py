#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Inherited from day 16.
class Device:
    def __init__(self, registers=[0]*6):
        self._registers = registers
        self._instruction_pointer = 0
        self._program = None
        self._program_length = 0

    def set_instruction_pointer(self, register):
        self._instruction_pointer = register

    def load_program(self, program):
        self._program = program
        self._program_length = len(program)

    def get_registers(self):
        return self._registers

    def set_registers(self, registers):
        self._registers = registers

    def _execute_instruction(self):
        instruction = self._program[self._registers[self._instruction_pointer]]
        getattr(self, instruction[0])(*instruction[1:])

    def execute_program(self, max_instructions=50000):
        count = 0
        last_instruction = 0

        while self._registers[self._instruction_pointer] < self._program_length and count < max_instructions:
            count += 1
            last_instruction = self._registers[self._instruction_pointer]
            self._execute_instruction()
            self._registers[self._instruction_pointer] += 1

        self._registers[self._instruction_pointer] = last_instruction

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


def read_problem_data(filename):
    instruction_pointer = 0
    program = list()

    with open(filename, "r") as f:
        for line in f:
            if "#ip" in line:
                instruction_pointer = int(line.split()[1])
            else:
                instruction, *data = line.split()
                program.append([instruction] + list(map(int, data)))

    return instruction_pointer, program


def main(_args):
    instruction_pointer, program = read_problem_data("day_19.txt")

    device = Device()
    device.set_instruction_pointer(instruction_pointer)
    device.load_program(program)
    device.execute_program()

    # Turns out, the program only sums the factors of the last register, but in a terribly inefficient manner. Which we
    # can do ourselves.
    last_register = device.get_registers()[-1]
    first_answer = sum(x for x in range(1, last_register+1) if last_register % x == 0)
    print("The first answer is: {}".format(first_answer))

    # Second problem. Reinitialize the device, but setting the first register (0) to 1.
    device.set_registers([1, 0, 0, 0, 0, 0])
    device.execute_program()

    last_register = device.get_registers()[-1]
    second_answer = sum(x for x in range(1, last_register + 1) if last_register % x == 0)
    print("The second answer is: {}".format(second_answer))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
