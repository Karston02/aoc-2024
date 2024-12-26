def read_file():
    """Read input"""
    with open("input.txt") as f:
        return f.read().strip()

def initialize_grid_and_robot(puzzle_input):
    """Initializes the grid and robot position from the puzzle input"""
    grid, directions = puzzle_input.split('\n\n')
    grid = [list(row) for row in grid.split('\n')]
    
    # find the robot's initial position
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '@':
                robot = (i, j)
                grid[i][j] = '.'
                return grid, robot, directions
    return grid, None, directions

def move_robot(grid, robot, direction):
    """Moves the robot in the specified direction"""
    i, j = robot
    if direction == '<':
        k = j - 1
        while grid[i][k] == 'O':
            k -= 1
        if grid[i][k] == '.':
            grid[i][k], grid[i][j - 1] = grid[i][j - 1], grid[i][k]
            return i, j - 1
    elif direction == '>':
        k = j + 1
        while grid[i][k] == 'O':
            k += 1
        if grid[i][k] == '.':
            grid[i][k], grid[i][j + 1] = grid[i][j + 1], grid[i][k]
            return i, j + 1
    elif direction == '^':
        k = i - 1
        while grid[k][j] == 'O':
            k -= 1
        if grid[k][j] == '.':
            grid[k][j], grid[i - 1][j] = grid[i - 1][j], grid[k][j]
            return i - 1, j
    elif direction == 'v':
        k = i + 1
        while grid[k][j] == 'O':
            k += 1
        if grid[k][j] == '.':
            grid[k][j], grid[i + 1][j] = grid[i + 1][j], grid[k][j]
            return i + 1, j
    return robot

def part1(puzzle_input):
    """Solves part 1 of the puzzle"""
    grid, robot, directions = initialize_grid_and_robot(puzzle_input)
    
    for direction in directions:
        robot = move_robot(grid, robot, direction)

    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'O':
                total += 100 * i + j  
  
    return total

def main():
    """Main function"""
    puzzle_input = read_file()
    result = part1(puzzle_input)
    print(result)

if __name__ == "__main__":
    main()
