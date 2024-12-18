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