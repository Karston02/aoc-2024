import re

def read_file():
    """Read input"""
    with open('input.txt', 'r') as file:
        return file.read()

def parse_machine(lines):
    """Parse a single machine's config from three lines of input"""
    # get numbers using regex
    a_moves = [int(x) for x in re.findall(r'\d+', lines[0])]
    b_moves = [int(x) for x in re.findall(r'\d+', lines[1])]
    prize_loc = [int(x) for x in re.findall(r'\d+', lines[2])]
    
    # returns a tuple of tuples
    return ((a_moves[0], a_moves[1]), (b_moves[0], b_moves[1]), (prize_loc[0], prize_loc[1]))

def parse_input(text):
    """Parse all machines from the input text"""
    machines = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            machines.append(parse_machine(lines[i:i+3]))
    
    return machines

def solve_machine(machine, max_presses=100):
    """
    Try to solve a single machine, returning (a_presses, b_presses) if possible.
    """
    a_moves, b_moves, prize = machine
    
    # try all combinations of button presses up to max_presses
    for a in range(max_presses + 1):
        for b in range(max_presses + 1):
            # check if this combination reaches the prize
            if (a * a_moves[0] + b * b_moves[0] == prize[0] and 
                a * a_moves[1] + b * b_moves[1] == prize[1]):
                return (a, b)
    # shouldn't happen w our input
    return None

def calculate_tokens(a_presses, b_presses):
    """Calculate total tokens needed for given button presses."""
    return 3 * a_presses + b_presses

def solve_puzzle(input_text):
    """Solve the entire puzzle, returning the minimum tokens needed."""
    machines = parse_input(input_text)
    total_tokens = 0

    # solve each machine and calculate tokens
    for machine in machines:
        solution = solve_machine(machine)
        if solution:
            tokens = calculate_tokens(*solution)
            total_tokens += tokens
            
    return total_tokens

def solve_machine_algebraically(machine):
    """Solve a machine using determinants for linear systems"""
    a_moves, b_moves, prize = machine
    px, py = prize
    
    ax, ay = a_moves
    bx, by = b_moves

    # solve using determinants for linear systems
    denominator = ax * by - bx * ay

    # compute presses for buttons A and B
    b_presses = (ax * py - px * ay) / denominator
    a_presses = (px - b_presses * bx) / ax if ax != 0 else (py - b_presses * by) / ay

    # ensure the solution is valid and integers
    if b_presses.is_integer() and a_presses.is_integer() and a_presses >= 0 and b_presses >= 0:
        return int(a_presses), int(b_presses)

    return None

def solve_puzzle_part2(input_text):
    """Solve the entire puzzle for part 2, returning the minimum tokens needed"""
    machines = parse_input(input_text)
    offset = 10**13
    total_tokens = 0

    # adjust prize coordinates by offset
    machines = [
        (a_moves, b_moves, (prize[0] + offset, prize[1] + offset))
        for a_moves, b_moves, prize in machines
    ]

    for machine in machines:
        solution = solve_machine_algebraically(machine)
        if solution:
            tokens = calculate_tokens(*solution)
            total_tokens += tokens

    return total_tokens

def main():
    """Main function"""
    input_text = read_file()
    result = solve_puzzle(input_text)
    print(f"Minimum tokens needed for part 1: {result}")

    result = solve_puzzle_part2(input_text)
    print(f"Minimum tokens needed for part 2: {result}")

if __name__ == "__main__":
    main()