from collections import deque

def read_file():
    """Reads input text file"""
    with open("input.txt") as f:
        return f.read().strip().splitlines()

def parse_input(data):
    """Parses input data"""
    rules = []
    updates = []
    for line in data:
        line = line.strip()  # strip any leading/trailing whitespace
        if "|" in line:
            rules.append(tuple(map(int, line.split("|"))))  # parse rule into a tuple of integers
        elif line:  # check if line isn't empty
            updates.append(list(map(int, line.split(","))))  # parse update into a list of integers

    return rules, updates

def check_order(rules, update):
    """
    Checks if the update is in the correct order based on the rules.
    Only considers rules where both pages are present in the update.
    """
    page_positions = {page: idx for idx, page in enumerate(update)}  # map each page to its index in dict
    for x, y in rules:
        if x in page_positions and y in page_positions:  # only consider rules relevant to the update
            if page_positions[x] > page_positions[y]:  # check order
                return False
    return True

def find_middle(update):
    """Finds the middle page number of the update"""
    return update[len(update) // 2]

def reorder_update(rules, update):
    """
    Reorders the update based on the rules. Uses a topological sort approach to
    reorder the pages in a valid order.
    """
    # create an in-degree counter and adjacency list
    in_degree = {page: 0 for page in update}
    adj = {page: [] for page in update}
    
    for x, y in rules:
        if x in in_degree and y in in_degree:  # only apply rules where both pages are present
            adj[x].append(y)
            in_degree[y] += 1

    # topo-sort (kahn's algo)
    queue = deque([page for page, degree in in_degree.items() if degree == 0])
    ordered = []

    while queue:
        page = queue.popleft()
        ordered.append(page)
        
        for neighbor in adj[page]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return ordered

def main():
    """Main function"""
    data = read_file()
    rules, updates = parse_input(data)
    
    valid_updates = []
    invalid_updates = []

    for update in updates:
        if check_order(rules, update):
            valid_updates.append(update)
        else:
            invalid_updates.append(update)
    
    middle_sum = sum(find_middle(update) for update in valid_updates)
    print("Sum of middle page numbers:", middle_sum)

    reordered_updates = [reorder_update(rules, update) for update in invalid_updates]
    print("Number of valid updates:", len(valid_updates))

    print("Sum of updated", sum(find_middle(update) for update in reordered_updates))

if __name__ == "__main__":
    main()
