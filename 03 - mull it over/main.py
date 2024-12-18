import re

def read_file():
    """Reads input text file."""
    with open("input.txt") as f:
        return f.read().strip()

def extract_instructions(input_data):
    """
    Extracts all relevant instructions from the input data in order.
    This includes `mul(X,Y)` and `do()/don't()` instructions.
    """
    # regex patterns for `mul(X,Y)` and `do()/don't()`
    mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    state_pattern = r"(do\(\)|don't\(\))"
    combined_pattern = f"{mul_pattern}|{state_pattern}"

    # find all matches and return as iter objects
    return re.finditer(combined_pattern, input_data)

def process_instruction(match, is_enabled):
    """
    Processes a single instruction match. If match and enabled, returns the result of multiplication.
    If match is do or don't, it updates the state of the mul instructions.
    """
    if match.group(1):  # mul(X,Y) group matched
        if is_enabled:
            x, y = int(match.group(1)), int(match.group(2))
            return x * y, is_enabled
        return 0, is_enabled
    elif match.group(3):  # do() or don't() group matched
        if match.group(3) == "do()":
            return 0, True
        elif match.group(3) == "don't()":
            return 0, False
    return 0, is_enabled

def calculate_total(instructions):
    """Calculates total sum of enabled `mul` results based on instructions."""
    total = 0
    is_enabled = True  # mul instructions are enabled to start

    for match in instructions:
        result, is_enabled = process_instruction(match, is_enabled)
        total += result

    return total

def main():
    """Main function."""
    input_data = read_file()
    instructions = extract_instructions(input_data)
    return calculate_total(instructions)

if __name__ == "__main__":
    print(main())