from collections import defaultdict

def read_file():
    """Read input"""
    with open("input.txt") as f:
        return f.read().strip()

def initialize_grid_and_robot(puzzle_input):
    """Initializes the grid and robot position from the puzzle input for part 1"""
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
    """Moves the robot in the specified direction for part 1"""
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

def initialize_part2_grid_and_robot(puzzle_input):
    """Initializes the grid and robot position for part 2"""
    grid, directions = puzzle_input.split('\n\n')
    grid = [list(row) for row in grid.split('\n')]
    m, n = len(grid), len(grid[0])
    
    # initialize the grid and find the robot's position
    for i in range(m):
        for j in reversed(range(n)):
            if grid[i][j] == '#':
                grid[i].insert(j, '#')
            if grid[i][j] == '.':
                grid[i].insert(j, '.')
            if grid[i][j] == '@':
                robot = (i, j * 2)  # adjust for grid expansion
                grid[i][j:j+1] = ['.', '.']
            if grid[i][j] == 'O':
                grid[i][j:j+1] = ['[', ']']
    return grid, robot, directions, m, n

def move_robot_part2(grid, robot, direction):
    """Moves the robot in the specified direction for part 2"""
    i, j = robot
    if direction == '<':
        k = j - 1
        while grid[i][k] == ']':
            k -= 2
        if grid[i][k] == '.':
            for l in range(k, j):
                grid[i][l] = grid[i][l + 1]
            return i, j - 1
    elif direction == '>':
        k = j + 1
        while grid[i][k] == '[':
            k += 2
        if grid[i][k] == '.':
            for l in reversed(range(j + 1, k + 1)):
                grid[i][l] = grid[i][l - 1]
            return i, j + 1
    elif direction == '^':
        return move_robot_up(grid, i, j)
    elif direction == 'v':
        return move_robot_down(grid, i, j)
    return robot

def move_robot_up(grid, i, j):
    """Moves the robot up in part 2"""
    queue = {(i - 1, j)}
    rows = defaultdict(set)
    while queue:
        x, y = queue.pop()
        match grid[x][y]:
            case '#':
                break
            case ']':
                rows[x] |= {y - 1, y}
                queue |= {(x - 1, y), (x - 1, y - 1)}
            case '[':
                rows[x] |= {y, y + 1}
                queue |= {(x - 1, y), (x - 1, y + 1)}
            case '.':
                rows[x].add(y)
    else:
        for x in sorted(rows):
            for y in rows[x]:
                grid[x][y] = grid[x + 1][y] if y in rows[x + 1] else '.'
        return i - 1, j
    return i, j

def move_robot_down(grid, i, j):
    """Moves the robot down in part 2"""
    queue = {(i + 1, j)}
    rows = defaultdict(set)
    while queue:
        x, y = queue.pop()
        match grid[x][y]:
            case '#':
                break
            case ']':
                rows[x] |= {y - 1, y}
                queue |= {(x + 1, y), (x + 1, y - 1)}
            case '[':
                rows[x] |= {y, y + 1}
                queue |= {(x + 1, y), (x + 1, y + 1)}
            case '.':
                rows[x].add(y)
    else:
        for x in sorted(rows, reverse=True):
            for y in rows[x]:
                grid[x][y] = grid[x - 1][y] if y in rows[x - 1] else '.'
        return i + 1, j
    return i, j

def part2(puzzle_input):
    """Solves part 2 of the puzzle"""
    grid, robot, directions, m, n = initialize_part2_grid_and_robot(puzzle_input)
    
    for direction in directions:
        robot = move_robot_part2(grid, robot, direction)

    total = 0
    for i in range(m):
        for j in range(n * 2):  # account for grid expansion
            if grid[i][j] == '[':
                total += 100 * i + j

    return total

def main():
    """Main function."""
    puzzle_input = read_file()
    result_part1 = part1(puzzle_input)
    print(f"Part 1 result: {result_part1}")
    result_part2 = part2(puzzle_input)
    print(f"Part 2 result: {result_part2}")

if __name__ == "__main__":
    main()
