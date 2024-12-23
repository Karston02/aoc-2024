from collections import defaultdict

def read_file():
    """Read input"""
    with open("input.txt", "r") as file:
        return [line.strip() for line in file.readlines()]
    
def build_adjacency_list(connections):
    """Builds an adjacency list from the connections"""
    graph = defaultdict(set)
    for connection in connections:
        a, b = connection.split("-")
        graph[a].add(b)
        graph[b].add(a)
    return graph

def find_interconnected_sets(connections):
    """Finds all sets of three interconnected computers"""
    graph = build_adjacency_list(connections)

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

def find_largest_clique(connections):
    """Finds the largest set of computers where each is connected to every other (a clique)."""
    graph = build_adjacency_list(connections)
    
    # bron-kerbosch algorithm for finding all maximal cliques
    def bron_kerbosch(r, p, x):
        if not p and not x:
            cliques.append(r)
            return
        for node in list(p):
            bron_kerbosch(r | {node}, p & graph[node], x & graph[node])
            p.remove(node)
            x.add(node)

    cliques = []
    bron_kerbosch(set(), set(graph.keys()), set())

    # find the largest clique
    largest_clique = max(cliques, key=len)
    return largest_clique

def main():
    """Main function"""
    connections = read_file()

    # sets of three interconnected computers
    sets_of_three = find_interconnected_sets(connections)
    sets_with_t = filter_by_t(sets_of_three)
    print(f"Total sets with at least one 't': {len(sets_with_t)}")

    # largest clique
    largest_clique = find_largest_clique(connections)
    password = ",".join(sorted(largest_clique))
    print(f"Password to the LAN party: {password}")

if __name__ == "__main__":
    main()
