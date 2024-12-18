def read_file():
    """Reads input text file"""
    with open("input.txt") as f:
        return f.read().strip()

def parse_map(map_input):
    """Parse the input map into a 2D grid and find initial guard position and direction"""
    grid = [list(row) for row in map_input.strip().split('\n')]
    
    directions = ['^', '>', 'v', '<']
    
    # find guard's initial pos & dir
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in directions:
                return grid, x, y, directions.index(cell)

def count_distinct_positions(map_input):
    """Count distinct positions visited by the guard before it leaves the grid"""
    grid, x, y, direction = parse_map(map_input)
    height, width = len(grid), len(grid[0])
    
    # tracking visited positions (no repeats)
    visited = set([(x, y)])
    
    moves = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]
    
    while True:
        # check if next position is valid and not an obstruction
        next_x = x + moves[direction][0]
        next_y = y + moves[direction][1]
        
        # check if out of bounds or hit an obstruction
        if (next_x < 0 or next_x >= width or 
            next_y < 0 or next_y >= height or 
            grid[next_y][next_x] == '#'):
            # turn right
            direction = (direction + 1) % 4
        else:
            # move forward
            x, y = next_x, next_y
            visited.add((x, y))
            
            # check if guard is completely outside the mapped area (end it)
            if (x <= 0 or x >= width - 1 or 
                y <= 0 or y >= height - 1):
                break
    
    return len(visited)

def main():
    """Main function"""
    grid = read_file()
    print(count_distinct_positions(grid))

if __name__ == '__main__':
    main()