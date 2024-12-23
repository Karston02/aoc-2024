from collections import defaultdict

def read_file():
    """Read input"""
    with open("input.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

def find_interconnected_sets(connections):
    """Finds all sets of three interconnected computers"""
    # build adjacency list
    graph = defaultdict(set)
    for connection in connections:
        a, b = connection.split("-")
        graph[a].add(b)
        graph[b].add(a)

    # find sets of three interconnected computers (triangles)
    sets_of_three = set()
    for node in graph:
        for neighbor in graph[node]:
            # ensure each edge processed only once
            if node < neighbor:
                # find common neighbors (intersection of two sets)
                common_neighbors = graph[node] & graph[neighbor]
                for common in common_neighbors:
                    trio = tuple(sorted([node, neighbor, common]))
                    sets_of_three.add(trio)

    return sets_of_three

def filter_by_t(sets_of_three):
    """Filters sets to include only those with at least one computer starting with t"""
    return [trio for trio in sets_of_three if any(computer.startswith('t') for computer in trio)]

def main():
    """Main function"""
    connections = read_file()
    sets_of_three = find_interconnected_sets(connections)
    sets_with_t = filter_by_t(sets_of_three)
    
    print(f"Total sets with at least one 't': {len(sets_with_t)}")

if __name__ == "__main__":
    main()
