"""
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise,
it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny
brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific
frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input)
of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............

The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas.
In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but
only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same
frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but
two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........

Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can
occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes
but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........

The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?


PART 2

Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency,
regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........

In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes
in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##

Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
"""
def read_file(file_path="input.txt"):
    """Read the input file and return a list of lines"""
    with open(file_path) as file:
        return [line.strip() for line in file]

def parse_input(map_data):
    """Parse the input map and organize data"""
    map_width = len(map_data[0])
    map_height = len(map_data)
    
    # storage for parsed data
    map_grid = {}
    frequency_groups = {}
    antenna_positions = []
    
    for y in range(map_height):
        for x in range(map_width):
            char = map_data[y][x]
            map_grid[(x, y)] = char
            
            if char != '.':
                # group antenna positions by their frequency
                frequency_groups.setdefault(char, set()).add((x, y))
                antenna_positions.append((x, y))
    
    return {
        "grid": map_grid,
        "width": map_width,
        "height": map_height,
        "frequencies": frequency_groups,
        "antennas": antenna_positions,
    }

def in_bounds(x, y, width, height):
    """Check if coordinates are within the map boundaries"""
    return 0 <= x < width and 0 <= y < height

def find_antinodes(frequency_groups, width, height):
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

    return antinode_locations

def calculate_signal_impact(map_data):
    """Calculate the number of unique antinodes within the map"""
    parsed_map = parse_input(map_data)
    
    # get antinode locations
    antinode_set = find_antinodes(
        parsed_map["frequencies"],
        parsed_map["width"],
        parsed_map["height"],
    )
    
    return len(antinode_set)

def main():
    map_data = read_file("input.txt")
    impact = calculate_signal_impact(map_data)
    print(f"Signal Impact: {impact}")

if __name__ == "__main__":
    main()
