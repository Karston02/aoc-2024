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
    
    # bfs
    while queue:
        pos, dist = queue.popleft() # (position, distance)
        r, c = pos
        
        # check all 4 directions
        for dr, dc in DIRECTIONS:
            new_r, new_c = r + dr, c + dc
            new_pos = (new_r, new_c)
            
            # valid position, not a wall, and not visited yet
            if (0 <= new_r < rows and 0 <= new_c < cols and 
                grid[new_r][new_c] in '.SE' and 
                new_pos not in distances):
                distances[new_pos] = dist + 1
                queue.append((new_pos, dist + 1))
    
    return distances

def find_cheats(grid, start, end, max_steps):
    """Find all cheats that save time"""
    rows, cols = len(grid), len(grid[0])
    
    start_distances = bfs_distances(grid, start)
    end_distances = bfs_distances(grid, end)
    
    base_time = start_distances[end]
    savings = defaultdict(int)
    
    # track unique cheats by start/end positions
    seen_cheats = set()
    
    for r1 in range(rows):
        for c1 in range(cols):
            if grid[r1][c1] not in '.SE':
                continue
                
            pos1 = (r1, c1)
            if pos1 not in start_distances:
                continue
                
            time_to_cheat = start_distances[pos1]
            
            seen = {pos1}
            queue = deque([(r1, c1, 0)])
            
            while queue:
                r2, c2, steps = queue.popleft()  # bfs for part 2
                pos2 = (r2, c2)
                
                if steps > max_steps:
                    continue
                
                if steps > 0 and grid[r2][c2] in '.SE' and pos2 in end_distances:
                    # only count each unique cheat (start/end position pair) once
                    cheat_key = (pos1, pos2)
                    # check if we haven't seen this cheat before
                    if cheat_key not in seen_cheats:
                        total_time = time_to_cheat + steps + end_distances[pos2]
                        if total_time < base_time:
                            savings[base_time - total_time] += 1
                            seen_cheats.add(cheat_key)
                
                if steps < max_steps:
                    for dr, dc in DIRECTIONS:
                        new_r, new_c = r2 + dr, c2 + dc
                        new_pos = (new_r, new_c)
                        
                        # valid position, not a wall, and not visited yet
                        if (0 <= new_r < rows and 0 <= new_c < cols and 
                            new_pos not in seen):
                            seen.add(new_pos)
                            queue.append((new_r, new_c, steps + 1))
    
    return savings

def solve_part1(grid, start, end):
    """Solve part 1: cheats up to 2 steps"""
    savings = find_cheats(grid, start, end, max_steps=2)
    return sum(count for saved, count in savings.items() if saved >= 100)

def solve_part2(grid, start, end):
    """Solve part 2: cheats up to 20 steps"""
    savings = find_cheats(grid, start, end, max_steps=20)
    return sum(count for saved, count in savings.items() if saved >= 100)

def main():
    """Main function"""
    grid = read_grid()
    start, end = find_start_end(grid)
    
    part1_result = solve_part1(grid, start, end)
    print(f"Part 1 - >= 100 picoseconds: {part1_result}")
    
    part2_result = solve_part2(grid, start, end)
    print(f"Part 2 - >= 100 picoseconds: {part2_result}")

if __name__ == "__main__":
    main()