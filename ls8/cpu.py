"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7
        self.stack = []

    def load(self):
        """Load a program into memory."""
        program = []
        f = open(sys.argv[1], "r")
        for line in f:
            li = line.strip()
            if not li.startswith("#"):
                if li != '':
                    curr = line.rstrip()
                    program.append(int(f'0b{curr.split()[0]}', 2))
        f.close()

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        def HLT(self, op, reg_a, reg_b):
            sys.exit(1)
            running = False

        def LDI(self, op, reg_a, reg_b):
            num = reg_b  # Get the num from 1st arg
            # Get the reg index from 2nd arg
            reg = reg_a
            self.reg[reg] = num  # Store the num in the right reg
            self.pc += 3

        def PRN(self, op, reg_a, reg_b):
            # Get the reg index from 1st arg
            reg = reg_a
            print(self.reg[reg])  # Print contents of that reg
            self.pc += 2

        def MUL(self, op, reg_a, reg_b):
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3

        def ADD(self, op, reg_a, reg_b):
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3

        def PUSH(self, op, reg_a, reg_b):
            value = self.reg[reg_a]
            self.reg[self.sp] -= 1
            self.ram[self.reg[self.sp]] = value
            self.pc += 2

        def POP(self, op, reg_a, reg_b):
            value = self.ram[self.reg[self.sp]]
            self.reg[reg_a] = value
            self.reg[self.sp] += 1
            self.pc += 2

        def CALL(self, op, reg_a, reg_b):
            self.stack.append(self.pc + 2)
            self.pc = self.reg[reg_a]

        def RET(self, op, reg_a, reg_b):
            value = self.stack[-1]
            del self.stack[-1]
            self.pc = value

        def exception(self, op, reg_a, reg_b):
            print('no valid Command')
            self.pc += 1

        instructions = {
            1: HLT,
            130: LDI,
            71: PRN,
            162: MUL,
            69: PUSH,
            70: POP,
            80: CALL,
            17: RET,
            160: ADD
        }

        while running:
            op = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]
            instructions[op](self, op, reg_a, reg_b)

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, value, mar):
        self.ram[mar] = value
