def read_file():
    """Read input"""
    with open('input.txt', 'r') as file:
        return file.read().strip()

def parse_schematics(data):
    """Parse the input data into locks and keys"""
    locks = []
    keys = []
    current_schematic = []
    
    for line in data.split('\n'):
        if line.strip():  # if line is not empty
            current_schematic.append(line)
        elif current_schematic:  # empty line and we have a schematic to process
            # check if it's a lock (filled top row) or key (empty top row)
            if current_schematic[0].startswith('#'):
                locks.append(current_schematic)
            else:
                keys.append(current_schematic)
            current_schematic = []
    
    # don't forget the last schematic if there's no trailing newline
    if current_schematic:
        if current_schematic[0].startswith('#'):
            locks.append(current_schematic)
        else:
            keys.append(current_schematic)
    
    return locks, keys

def get_heights(schematic, is_lock=True):
    """Convert a schematic to a list of column heights"""
    heights = []
    width = len(schematic[0])
    height = len(schematic)
    
    for col in range(width):
        column_height = 0
        if is_lock:
            # for locks, count from top until we find a '.'
            for row in range(height):
                if schematic[row][col] == '#':
                    column_height += 1
                else:
                    break
            heights.append(column_height)
        else:
            # for keys, count from bottom until we find a '.'
            for row in range(height - 1, -1, -1):
                if schematic[row][col] == '#':
                    column_height += 1
                else:
                    break
            heights.append(column_height)
    
    return heights

def can_fit(lock_heights, key_heights):
    """Check if a lock and key can fit together"""
    if len(lock_heights) != len(key_heights):
        return False
    
    # each column's combined height can't exceed height of the grid (7)
    for lock, key in zip(lock_heights, key_heights):
        if lock + key > 7:
            return False
    return True

def count_fitting_pairs(data):
    """Count the number of unique lock/key pairs that fit together"""
    # parse the input into locks and keys
    locks, keys = parse_schematics(data)
    
    # convert schematics to heights
    lock_heights = [get_heights(lock, True) for lock in locks]
    key_heights = [get_heights(key, False) for key in keys]
    
    # count fitting pairs
    fitting_pairs = 0
    for lock in lock_heights:
        for key in key_heights:
            if can_fit(lock, key):
                fitting_pairs += 1
    
    return fitting_pairs

def main():
    """Main function"""
    data = read_file()
    result = count_fitting_pairs(data)
    print(f"Number of unique lock/key pairs that fit: {result}")

if __name__ == "__main__":
    main()