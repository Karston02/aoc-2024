import heapq

# directions and their movements (dx, dy)
DIRECTIONS = ['E', 'S', 'W', 'N']
DIR_MOVES = {
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
    'N': (-1, 0)
}

def read_input():
    """Go through maze input and locate start (S) and end (E) positions"""
    with open("input.txt", 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]
    
    start = end = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    return grid, start, end

def turn(direction, turn_type):
    """Turn 90 degrees"""
    idx = DIRECTIONS.index(direction)
    if turn_type == 'clockwise':
        return DIRECTIONS[(idx + 1) % 4]
    elif turn_type == 'counterclockwise':
        return DIRECTIONS[(idx - 1) % 4]

def is_valid(grid, x, y):
    """Check if a position is within bounds and not a wall"""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'

def find_lowest_score():
    """Find the lowest score to navigate the maze"""
    grid, start, end = read_input()
    start_x, start_y = start
    end_x, end_y = end
    
    # priority queue for A* search: (cost, x, y, direction)
    heap = [(0, start_x, start_y, 'E')]
    visited = set()  # keep track of visited states (x, y, direction)
    
    while heap:
        cost, x, y, direction = heapq.heappop(heap)
        
        # if we reach the end position, return cost
        if (x, y) == (end_x, end_y):
            return cost
        
        # skip if already visited
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))
        
        # move forward in the current direction
        dx, dy = DIR_MOVES[direction]
        new_x, new_y = x + dx, y + dy
        if is_valid(grid, new_x, new_y):
            heapq.heappush(heap, (cost + 1, new_x, new_y, direction))
        
        # rotate clockwise and counterclockwise
        clockwise_dir = turn(direction, 'clockwise')
        counterclockwise_dir = turn(direction, 'counterclockwise')
        
        heapq.heappush(heap, (cost + 1000, x, y, clockwise_dir))
        heapq.heappush(heap, (cost + 1000, x, y, counterclockwise_dir))
    
    return -1  # no path (shouldn't happen)

def main():
    """Main function"""
    result = find_lowest_score()
    print(f"Lowest Score: {result}")

if __name__ == "__main__":
    main()