def read_input():
    """Reads the input file"""
    with open("input.txt", 'r') as file:
        lines = file.readlines()

    # extract registers
    register_a = int(lines[0].split(":")[1].strip())
    register_b = int(lines[1].split(":")[1].strip())
    register_c = int(lines[2].split(":")[1].strip())

    # extract program
    program = list(map(int, lines[4].split(":")[1].strip().split(',')))

    return register_a, register_b, register_c, program


def execute_program(register_a, register_b, register_c, program):
    """Executes the program based on the 3-bit computer instructions"""
    registers = {'A': register_a, 'B': register_b, 'C': register_c}

    ip = 0
    output = []

    # instructions loop
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        # opcode handling
        if opcode == 0:  # adv: divide A by 2^operand (combo operand)
            value = combo_operand_value(operand, registers)
            registers['A'] //= (2 ** value)

        elif opcode == 1:  # bxl: B XOR literal operand
            registers['B'] ^= operand

        elif opcode == 2:  # bst: set B to combo operand % 8
            value = combo_operand_value(operand, registers)
            registers['B'] = value % 8

        elif opcode == 3:  # jnz: jump to literal operand if A != 0
            if registers['A'] != 0:
                ip = operand
                continue  # Skip IP increment for this instruction

        elif opcode == 4:  # bxc: B XOR C (ignores operand)
            registers['B'] ^= registers['C']

        elif opcode == 5:  # out: output combo operand % 8
            value = combo_operand_value(operand, registers)
            output.append(value & 7)  # Use bitwise AND for clarity (same as % 8)

        elif opcode == 6:  # bdv: divide A by 2^operand, store in B
            value = combo_operand_value(operand, registers)
            registers['B'] = registers['A'] // (2 ** value)

        elif opcode == 7:  # cdv: divide A by 2^operand, store in C
            value = combo_operand_value(operand, registers)
            registers['C'] = registers['A'] // (2 ** value)

        # increment instruction pointer by 2
        ip += 2

    return output

def combo_operand_value(operand, registers):
    """
    Returns the value of a combo operand.
    Operands 0-3 return literal values
    Operands 4-6 return register values A, B, or C
    """
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']

def main():
    """Main function"""
    # read input
    register_a, register_b, register_c, program = read_input()

    # run the program
    output = execute_program(register_a, register_b, register_c, program)

    # join output values with commas for submission
    result = ",".join(map(str, output))

    print("Output:", result)

if __name__ == "__main__":
    main()