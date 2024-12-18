DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def read_file():
    """Reads input"""
    with open("input.txt", 'r') as file:
        return [line.strip() for line in file.readlines()]

def parse_map(map_data):
    """Parses the input map data into a 2D list of integers"""
    return [[int(char) for char in line] for line in map_data]

def find_trailheads(topographic_map):
    """Finds all trailheads (positions with height 0)"""
    trailheads = []
    # loop through the map to find all trailheads
    for row in range(len(topographic_map)):
        for col in range(len(topographic_map[row])):
            # for each row, find trailhead
            if topographic_map[row][col] == 0:
                trailheads.append((row, col)) # location of trailhead
    return trailheads

def is_valid_move(topographic_map, current, next_pos):
    """Checks if moving to the next position is valid"""
    rows, cols = len(topographic_map), len(topographic_map[0])
    r, c = next_pos
    # check if next position is within bounds and is 1 greater than current position
    if 0 <= r < rows and 0 <= c < cols:
        return topographic_map[next_pos[0]][next_pos[1]] == topographic_map[current[0]][current[1]] + 1
    return False

def bfs_trail_score(topographic_map, start):
    """Performs BFS from a trailhead to calculate its score"""
    queue = [start]
    visited = set()
    visited.add(start)
    reachable_nines = set()

    while queue:
        current = queue.pop(0)
        row, col = current

        # check if current position is height 9
        if topographic_map[row][col] == 9:
            reachable_nines.add(current)

        # explore neighbors (up, down, left, right)
        for dr, dc in DIRECTIONS:
            next_pos = (row + dr, col + dc)
            # if next position is not visited and is a valid move
            if next_pos not in visited and is_valid_move(topographic_map, current, next_pos):
                visited.add(next_pos)
                queue.append(next_pos)

    return len(reachable_nines)

def dfs_count_trails(topographic_map, current):
    """Performs DFS to count distinct hiking trails starting from a given position"""
    row, col = current

    # base case: if we reach height 9, it's a distinct trail
    if topographic_map[row][col] == 9:
        return 1

    total_trails = 0

    # explore neighbors (up, down, left, right)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_pos = (row + dr, col + dc)
        if is_valid_move(topographic_map, current, next_pos):
            total_trails += dfs_count_trails(topographic_map, next_pos)

    return total_trails

def calculate_total_score(topographic_map):
    """Calculates the total score of all trailheads in the map"""
    trailheads = find_trailheads(topographic_map)
    total_score = 0

    for trailhead in trailheads:
        total_score += bfs_trail_score(topographic_map, trailhead)

    return total_score

def calculate_total_rating(topographic_map):
    """Calculates the total rating of all trailheads in the map"""
    trailheads = find_trailheads(topographic_map)
    total_rating = 0

    for trailhead in trailheads:
        total_rating += dfs_count_trails(topographic_map, trailhead)

    return total_rating

def main():
    map_data = read_file()
    topographic_map = parse_map(map_data)

    # calculate and print the total score of all trailheads
    total_score = calculate_total_score(topographic_map)
    print(f"Total Score of all trailheads: {total_score}")

    # calculate and print the total rating of all trailheads
    total_rating = calculate_total_rating(topographic_map)
    print(f"Total Rating of all trailheads: {total_rating}")

if __name__ == "__main__":
    main()
