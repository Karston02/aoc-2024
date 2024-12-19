def read_file():
    """Reads input"""
    with open("input.txt", "r") as file:
        return file.read()

def parse_input(input_data):
    """Parses the input data into towel patterns and designs"""
    towel_patterns_section, designs_section = input_data.split('\n\n')
    towel_patterns = towel_patterns_section.split(', ')
    designs = designs_section.split('\n')
    return towel_patterns, designs

def can_form_design(design, towel_patterns):
    """
    Determines if a design string can be formed by concatenating
    the available towel patterns
    
    Uses DP to check if we can build the design left -> right
    using the available towel patterns
    """
    # will be true if the first i characters of the design can be formed
    dp = [False] * (len(design) + 1)
    dp[0] = True
    
    # go thru each position in the design
    for i in range(1, len(design) + 1):
        # for each position, check all possible patterns
        for towel in towel_patterns:
            # check if the towel can fit at the current position i
            if i >= len(towel) and design[i-len(towel):i] == towel:
                # if the previous part of the design (before the towel) is formable
                # (dp[i - len(towel)]), then this part can be formable too.
                dp[i] = dp[i] or dp[i - len(towel)]
    
    # if this is true, the entire design can be formed.
    return dp[len(design)]

def count_possible_designs(designs, towel_patterns):
    """Counts how many designs can be formed using the towel patterns"""
    possible_count = 0
    for design in designs:
        if can_form_design(design, towel_patterns):
            possible_count += 1
    
    return possible_count


def main():
    """Main function"""
    input_data = read_file()
    towel_patterns, designs = parse_input(input_data)
    print(count_possible_designs(designs, towel_patterns))

if __name__ == "__main__":
    main()
