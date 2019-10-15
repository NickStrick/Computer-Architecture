"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0
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

        address = 0
        self.ram = [0] * (len(program)+2)
        # print(program, len(program), self.ram)

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        # elif op == "SUB": etc
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
        HLT = 1
        LDI = 130
        PRN = 71
        MUL = 162
        PUSH = 69
        POP = 70
        CALL = 80
        RET = 17
        ADD = 160
        running = True

        while running:
            # Do stuff
            # print(self.pc)
            op = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc+2]
            if op == HLT:
                sys.exit(1)
                running = False
            elif op == LDI:
                num = reg_b  # Get the num from 1st arg
                # Get the reg index from 2nd arg
                reg = reg_a
                self.reg[reg] = num  # Store the num in the right reg
                self.pc += 3
            elif op == PRN:
                # Get the reg index from 1st arg
                reg = reg_a
                print(self.reg[reg])  # Print contents of that reg
                self.pc += 2
            elif op == MUL:
                self.reg[reg_a] *= self.reg[reg_b]
                self.pc += 3
            elif op == ADD:
                self.reg[reg_a] += self.reg[reg_b]
                self.pc += 3
            elif op == PUSH:
                self.stack.append(self.reg[reg_a])
                self.pc += 2
            elif op == POP:
                value = self.stack[-1]
                del self.stack[-1]
                self.reg[reg_a] = value
                self.pc += 2
            elif op == CALL:
                self.stack.append(self.pc + 2)
                self.pc = self.reg[reg_a]

            elif op == RET:
                value = self.stack[-1]
                del self.stack[-1]
                self.pc = value

            else:
                print('no valid Command')
                self.pc += 1

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, value, mar):
        self.ram[mar] = value
