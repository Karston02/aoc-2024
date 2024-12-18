from collections import deque

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def read_file():
    """Read input"""
    with open("input.txt", "r") as file:
        return [tuple(map(int, line.strip().split(','))) for line in file]

def simulate_memory_space(byte_positions):
    """
    Simulates the memory space after bytes fall.
    """
    corrupted = set()
    for x, y in byte_positions:
        corrupted.add((x, y))
    return corrupted

def bfs_shortest_path(corrupted, grid_size=71):
    """
    Finds the shortest path from (0,0) to (grid_size-1,grid_size-1) using BFS.
    """
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)
    queue = deque([(start, 0)])  # (current_position, steps)
    visited = set()
    visited.add(start)

    while queue:
        (x, y), steps = queue.popleft()

        # if we've reached the end, return the steps taken
        if (x, y) == end:
            return steps

        # explore neighbors
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:  # stay within bounds
                # if the neighbor is not corrupted and not visited
                if (nx, ny) not in corrupted and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), steps + 1))

    # if no path exists (shouldn't happen w/ input)
    return -1

def find_blocking_byte(byte_positions, grid_size=71):
    """Finds the first byte that blocks the path to the exit"""
    corrupted = set()

    for x, y in byte_positions:
        corrupted.add((x, y))

        # check if there's still a path to the exit
        if bfs_shortest_path(corrupted, grid_size) == -1:
            return (x, y)

    return None  # this shouldn't happen with our input, just in case

def main():
    byte_positions = read_file()

    # memory space with corrupted positions and find the shortest path
    corrupted = simulate_memory_space(byte_positions[:1024])
    shortest_path = bfs_shortest_path(corrupted)
    print(f"Minimum Steps: {shortest_path}")

    # find the first blocking byte
    blocking_byte = find_blocking_byte(byte_positions)
    print(f"First Blocking Byte: {blocking_byte[0]},{blocking_byte[1]}")

if __name__ == "__main__":
    main()
