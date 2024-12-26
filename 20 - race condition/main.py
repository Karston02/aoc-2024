from collections import deque, defaultdict

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def read_grid():
    """Read input"""
    grid = []
    with open("input.txt") as f:
        for line in f:
            grid.append(list(line.strip()))
    return grid

def find_start_end(grid):
    """Find start and end positions"""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                end = (i, j)
    return start, end

def bfs_distances(grid, start):
    """Calculate distances from start to all points using bfs"""
    rows, cols = len(grid), len(grid[0])
    distances = {}
    queue = deque([(start, 0)])
    distances[start] = 0
    
    # while there are still positions to visit
    while queue:
        pos, dist = queue.popleft() # get next pos
        r, c = pos
        
        # try all neighbors
        for dr, dc in DIRECTIONS:
            new_r, new_c = r + dr, c + dc
            new_pos = (new_r, new_c)
            
            # if valid position and not visited yet
            if (0 <= new_r < rows and 0 <= new_c < cols and 
                grid[new_r][new_c] in '.SE' and 
                new_pos not in distances):
                distances[new_pos] = dist + 1
                queue.append((new_pos, dist + 1))
    
    return distances

def find_cheats(grid, start, end):
    """Find all cheats that save time"""
    rows, cols = len(grid), len(grid[0])
    
    # calculate distances from start and end to all points
    start_distances = bfs_distances(grid, start)
    end_distances = bfs_distances(grid, end)
    
    if end not in start_distances:
        return defaultdict(int)  # no path exists
        
    base_time = start_distances[end]
    savings = defaultdict(int)
    
    # for each valid position that can be reached
    for r1 in range(rows):
        for c1 in range(cols):
            if grid[r1][c1] not in '.SE':
                continue
                
            pos1 = (r1, c1)
            if pos1 not in start_distances:
                continue
                
            time_to_cheat = start_distances[pos1]
            
            # try all positions within 2 steps (including through walls)
            seen = {pos1}
            stack = [(r1, c1, 0)]
            
            while stack:
                r2, c2, steps = stack.pop()
                pos2 = (r2, c2)
                
                if steps > 2:
                    continue
                
                # check if we can reach the end in time
                if steps > 0 and grid[r2][c2] in '.SE' and pos2 in end_distances:
                    total_time = time_to_cheat + steps + end_distances[pos2]
                    if total_time < base_time:
                        savings[base_time - total_time] += 1
                
                # add all neighbors
                if steps < 2:
                    for dr, dc in DIRECTIONS:
                        new_r, new_c = r2 + dr, c2 + dc
                        new_pos = (new_r, new_c)
                        
                        # only add if not seen before
                        if (0 <= new_r < rows and 0 <= new_c < cols and 
                            new_pos not in seen):
                            seen.add(new_pos)
                            stack.append((new_r, new_c, steps + 1))
    
    return savings

def solve():
    """Solve the problem"""
    grid = read_grid()
    start, end = find_start_end(grid)
    savings = find_cheats(grid, start, end)
    return sum(count for saved, count in savings.items() if saved >= 100)

def main():
    """Main function"""
    result = solve()
    print(f"Number of cheats saving ≥100 picoseconds: {result}")

if __name__ == "__main__":
    main()