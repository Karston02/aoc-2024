def read_file():
    """Read input"""
    with open("input.txt", "r") as file:
        return file.read().strip()

def parse_input(input_data):
    """Parse input data"""
    sections = input_data.split("\n\n")
    wire_values = {}
    gate_instructions = []

    # parse initial wire values
    for line in sections[0].split("\n"):
        wire, value = line.split(": ")
        wire_values[wire] = int(value)

    # parse gate instructions
    for line in sections[1].split("\n"):
        gate_instructions.append(line)

    return wire_values, gate_instructions

def evaluate_gates(wire_values, gate_instructions):
    """Evaluate all logic gates and resolve wire values"""
    unresolved_instructions = gate_instructions[:]
    resolved = set(wire_values.keys())

    while unresolved_instructions:
        next_round_instructions = []
        for instruction in unresolved_instructions:
            parts = instruction.split(" -> ")
            operation, output_wire = parts[0], parts[1]

            try:
                # ensure that inputs are available
                if " AND " in operation:
                    a, b = operation.split(" AND ")
                    if a in wire_values and b in wire_values:
                        wire_values[output_wire] = wire_values[a] & wire_values[b]
                        resolved.add(output_wire)
                    else:
                        next_round_instructions.append(instruction)

                elif " OR " in operation:
                    a, b = operation.split(" OR ")
                    if a in wire_values and b in wire_values:
                        wire_values[output_wire] = wire_values[a] | wire_values[b]
                        resolved.add(output_wire)
                    else:
                        next_round_instructions.append(instruction)

                elif " XOR " in operation:
                    a, b = operation.split(" XOR ")
                    if a in wire_values and b in wire_values:
                        wire_values[output_wire] = wire_values[a] ^ wire_values[b]
                        resolved.add(output_wire)
                    else:
                        next_round_instructions.append(instruction)

            except KeyError:
                # skip for now if one of the input wires is not yet resolved
                next_round_instructions.append(instruction)

        unresolved_instructions = next_round_instructions

    return wire_values

def calculate_output(wire_values):
    """Calculate the final output number"""
    # collect wires starting with z
    z_wires = {}
    for key, value in wire_values.items():
        if key.startswith('z'):
            z_wires[key] = value
    
    # sort z wires by their numeric part
    sorted_z_wires = []
    for key, value in z_wires.items():
        # extract the numeric part of the wire name (i.e. z00 -> 0)
        numeric_part = int(key[1:])
        sorted_z_wires.append((numeric_part, value))
    
    # sort the wires by the numeric part
    sorted_z_wires.sort()
    
    # build the binary number from the sorted wires (starting from least significant bit)
    binary_number = ""
    for numeric_part, value in reversed(sorted_z_wires):
        binary_number += str(value)
    
    # convert the binary number to decimal
    decimal_number = int(binary_number, 2)

    return binary_number, decimal_number

def main():
    """Main function"""
    input_data = read_file()

    # parse input data
    wire_values, gate_instructions = parse_input(input_data)

    # evaluate all gates
    wire_values = evaluate_gates(wire_values, gate_instructions)

    # calculate the output number
    binary_output, decimal_output = calculate_output(wire_values)

    print(f"Binary Output: {binary_output}")
    print(f"Decimal Output: {decimal_output}")

if __name__ == "__main__":
    main()
