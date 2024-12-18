def read_file(file_path="input.txt"):
    """Read the input file and return a list of lines"""
    with open(file_path) as file:
        return [line.strip() for line in file]

def parse_input(map_data):
    """Parse the input map and organize data"""
    
    # storage for parsed data
    map_grid = {}
    frequency_groups = {}
    antenna_positions = []
    
    for y in range(len(map_data[0])):
        for x in range(len(map_data)):
            char = map_data[y][x]
            map_grid[(x, y)] = char
            
            if char != '.':
                # group antenna positions by their frequency
                frequency_groups.setdefault(char, set()).add((x, y))
                antenna_positions.append((x, y))
    
    return {
        "grid": map_grid,
        "width": len(map_data[0]),
        "height": len(map_data),
        "frequencies": frequency_groups,
        "antennas": antenna_positions,
    }

def in_bounds(x, y, width, height):
    """Check if coordinates are within the map boundaries"""
    return 0 <= x < width and 0 <= y < height

def find_antinodes(frequency_groups, width, height, include_self=True):
    """Find all unique antinode locations"""
    antinode_locations = set()
    
    for _, positions in frequency_groups.items():
        positions = list(positions)
        num_positions = len(positions)
        
        # examine all pairs of antennas with the same frequency
        for i in range(num_positions):
            for j in range(i + 1, num_positions):
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                
                # get direction vector
                dx, dy = x2 - x1, y2 - y1
                
                # get antinodes for this pair
                candidate_antinodes = [
                    (x1 - dx, y1 - dy),  # before the first antenna
                    (x2 + dx, y2 + dy),  # after the second antenna
                ]
                
                # add valid ones to the antinode set
                antinode_locations.update(
                    (x, y) for x, y in candidate_antinodes if in_bounds(x, y, width, height)
                )
        if include_self and num_positions > 1:
            # include antenna positions as antinodes if they align with others
            antinode_locations.update(positions)

    return antinode_locations

def calculate_signal_impact(map_data, include_self=True):
    """Calculate the number of unique antinodes within the map"""
    parsed_map = parse_input(map_data)
    
    # get antinode locations
    antinode_set = find_antinodes(
        parsed_map["frequencies"],
        parsed_map["width"],
        parsed_map["height"],
        include_self
    )
    
    return len(antinode_set)

def main():
    map_data = read_file("input.txt")
    impact = calculate_signal_impact(map_data, include_self=False)
    print(f"Signal Impact: {impact}")
    print(f"Signal Impact w/ Self: {calculate_signal_impact(map_data)}")

if __name__ == "__main__":
    main()
