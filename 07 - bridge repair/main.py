"""
The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge,
though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.)
You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing
nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could
determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether
the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be
rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would
give the est value (10 * 19 = 190).
3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side
to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly
be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?


PART 2

The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances.
Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345
would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three
more equations that can be made true by inserting operators:

156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
192: 17 8 14 can be made true using 17 || 8 + 14.
Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by
also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?
"""
def evaluate_expression(numbers, operators):
    """Evaluate an expression with given numbers and operators
    following left-to-right evaluation"""
    # start with the first number
    result = numbers[0]
    
    # apply operators left to right
    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        elif op == '*':
            result *= numbers[i + 1]
        elif op == '||':
            result = int(str(result) + str(numbers[i + 1]))
    
    return result

def can_solve_equation(line):
    """Determine if an equation can be solved using operators"""
    # parse line
    test_value, number_str = line.split(': ')
    test_value = int(test_value)
    numbers = list(map(int, number_str.split()))
    
    # try all possible operator combinations (just + and *)
    operators = ['+', '*', '||']
    
    # generate all possible operator configurations
    def generate_operator_configs(length):
        if length == 1:
            return [[op] for op in operators]
        
        configs = []
        for first_ops in generate_operator_configs(length - 1):
            for op in operators:
                configs.append(first_ops + [op])
        return configs
    
    # num of operator slots is length of numbers - 1 (the spaces)
    op_configs = generate_operator_configs(len(numbers) - 1)
    
    # try each configuration
    for op_config in op_configs:
        result = evaluate_expression(numbers, op_config)
        if result == test_value:
            return True
    
    return False

def solve_calibration(filename):
    """Solve the puzzle by finding valid equations and summing"""
    solvable_total = 0
    solvable_equations = []
    
    # read the file and process each line
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if can_solve_equation(line):
                test_value = int(line.split(': ')[0])
                solvable_total += test_value
                solvable_equations.append(line)
    
    return solvable_total

def main():
    """Main function"""
    result = solve_calibration('input.txt')
    print(f"Total calibration result: {result}")

if __name__ == '__main__':
    main()