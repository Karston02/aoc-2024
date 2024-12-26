from dataclasses import dataclass

@dataclass
class Operation:
    input1: str
    operator: str
    input2: str
    result: str

class CircuitProcessor:
    def __init__(self, input_file):
        self.wires = {}
        self.operations = []
        self.wrong_wires = set()
        self.highest_z_wire = "z00"
        self.load_circuit(input_file)

    def load_circuit(self, input_file):
        """Load and parse circuit data from input file"""
        data = open(input_file).read().split("\n")
        for line in self.parse_circuit_data(data):
            if ":" in line:
                self.process_wire_assignment(line)
            elif "->" in line:
                self.process_operation(line)

    def parse_circuit_data(self, data):
        """Remove empty lines and comments from input data"""
        return [line.strip() for line in data if line.strip()]

    def process_wire_assignment(self, line):
        """Process direct wire value assignments"""
        wire, value = line.split(": ")
        self.wires[wire] = int(value)

    def process_operation(self, line):
        """Process circuit operations and update highest z wire"""
        input1, operator, input2, _, result = line.split(" ")
        operation = Operation(input1, operator, input2, result)
        self.operations.append(operation)
        
        if result.startswith('z'):
            current_z_value = int(result[1:])
            highest_z_value = int(self.highest_z_wire[1:])
            if current_z_value > highest_z_value:
                self.highest_z_wire = result

    @staticmethod
    def execute_operation(op, val1, val2):
        """Execute logical operations on two values"""
        operations = {
            "AND": lambda x, y: x & y,
            "OR": lambda x, y: x | y,
            "XOR": lambda x, y: x ^ y
        }
        return operations[op](val1, val2)

    def identify_wrong_wires(self):
        """Identify incorrectly connected wires based on circuit rules"""
        for op in self.operations:
            self._check_z_wire_rule(op)
            self._check_xor_wire_rule(op)
            self._check_and_wire_rule(op)
            self._check_xor_or_rule(op)

    def _check_z_wire_rule(self, op):
        """Check if z-wires follow correct operation rules"""
        if op.result.startswith('z') and op.operator != "XOR" and op.result != self.highest_z_wire:
            self.wrong_wires.add(op.result)

    def _check_xor_wire_rule(self, op):
        """Check if XOR operations use correct wire types"""
        if (op.operator == "XOR" and 
            not any(w.startswith(('x', 'y', 'z')) for w in [op.result, op.input1, op.input2])):
            self.wrong_wires.add(op.result)

    def _check_and_wire_rule(self, op):
        """Check if AND operations follow circuit rules"""
        if op.operator == "AND" and "x00" not in [op.input1, op.input2]:
            for subop in self.operations:
                if ((op.result == subop.input1 or op.result == subop.input2) 
                    and subop.operator != "OR"):
                    self.wrong_wires.add(op.result)

    def _check_xor_or_rule(self, op):
        """Check if XOR outputs are used correctly with OR operations"""
        if op.operator == "XOR":
            for subop in self.operations:
                if ((op.result == subop.input1 or op.result == subop.input2) 
                    and subop.operator == "OR"):
                    self.wrong_wires.add(op.result)

    def process_circuit(self):
        """Process all circuit operations until all wires have values"""
        while self.operations:
            op = self.operations.pop(0)
            if op.input1 in self.wires and op.input2 in self.wires:
                self.wires[op.result] = self.execute_operation(
                    op.operator,
                    self.wires[op.input1],
                    self.wires[op.input2]
                )
            else:
                self.operations.append(op)

    def get_z_wire_value(self):
        """Get final binary value from z-wires"""
        z_bits = [
            str(self.wires[wire])
            for wire in sorted(self.wires, reverse=True)
            if wire.startswith('z')
        ]
        return int("".join(z_bits), 2)

    def get_wrong_wires(self):
        """Get comma-separated string of wrong wires"""
        return ",".join(sorted(self.wrong_wires))

def main():
    processor = CircuitProcessor("input.txt")
    processor.identify_wrong_wires()
    processor.process_circuit()
    
    print(processor.get_z_wire_value())
    print(processor.get_wrong_wires())

if __name__ == "__main__":
    main()