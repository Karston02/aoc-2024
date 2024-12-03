"""
"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse,
though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been
jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are
each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they
look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

PART 2


As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some
of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because
there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled
by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?
"""
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