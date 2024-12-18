DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def read_file():
    """Reads input"""
    with open("input.txt", "r") as file:
        return [line.strip() for line in file]

def parse(inputs):
    """Parse input into a map with coordinates"""
    map_dict = {}
    width = len(inputs[0])
    height = len(inputs)

    # create a dictionary of coordinates to plant types
    for y in range(height):
        for x in range(width):
            map_dict[(x, y)] = inputs[y][x]

    # return the map and dimensions
    return {"map": map_dict, "width": width, "height": height}

def flood_fill(map_dict, x, y, plant_type):
    """Flood fill to find a region of connected cells"""
    region = set()
    seen = set()
    queue = [(x, y)]

    # bfs to find connected cells
    while queue:
        curr_x, curr_y = queue.pop(0)

        if (curr_x, curr_y) in seen:
            continue

        seen.add((curr_x, curr_y))

        # check if the cell is the same type as the region
        if map_dict.get((curr_x, curr_y)) == plant_type:
            region.add((curr_x, curr_y))
            for dx, dy in DIRS:
                queue.append((curr_x + dx, curr_y + dy))

    return region

def get_regions(map_dict, width, height):
    """Find all regions in the map"""
    regions = []
    seen = set()

    # iterate through all cells in the map
    for x in range(width):
        for y in range(height):
            if (x, y) in seen:
                continue

            # find the region of connected cells
            region = flood_fill(map_dict, x, y, map_dict[(x, y)])
            seen.update(region)

            # add the region to the list of regions
            regions.append({
                "regionSet": region,
                "regionList": list(region),
                "regionType": map_dict[(x, y)],
            })
    return regions

def get_perimeter(map_dict, region):
    """Calculate the perimeter of a region"""
    perimeter = 0
    for x, y in region["regionList"]:
        for dx, dy in DIRS:
            neighbor = (x + dx, y + dy)
            # check if the neighbor is outside the region
            if map_dict.get(neighbor) != region["regionType"]:
                perimeter += 1
    return perimeter

def get_corners(width, height, region):
    """Calculate the number of sides/corners for a region."""
    num_corners = 0

    for x in range(-1, width):
        for y in range(-1, height):
            # check the four corners around this point
            corner_pts = []
            for dx, dy in [(0, 0), (1, 0), (1, 1), (0, 1)]:
                corner_key = (x + dx, y + dy)
                corner_pts.append('1' if corner_key in region["regionSet"] else '0')

            corner_str = ''.join(corner_pts)

            # determine corners based on the pattern (taken from Tim Trinidad's solution)
            if corner_str in ['1000', '0100', '0010', '0001', '0111', '1011', '1101', '1110']:
                num_corners += 1
            elif corner_str in ['1010', '0101']:
                num_corners += 2

    return num_corners

def calculate_with_perimeter(parsed):
    """Calculate total price using perimeter."""
    # get all the regions in the map
    regions = get_regions(parsed["map"], parsed["width"], parsed["height"])
    total_price = 0

    # calculate the price for each region based on its perimeter
    for region in regions:
        region_size = len(region["regionSet"])
        perimeter = get_perimeter(parsed["map"], region)
        total_price += region_size * perimeter

    return total_price


def calculate_with_corner(parsed):
    """Calculate total price using corner/side count."""
    # get all the regions in the map
    regions = get_regions(parsed["map"], parsed["width"], parsed["height"])
    total_price = 0

    # calculate the price for each region based on its corner count
    for region in regions:
        region_size = len(region["regionSet"])
        corners = get_corners(parsed["width"], parsed["height"], region)
        total_price += region_size * corners

    return total_price

def main():
    inputs = read_file()
    parsed = parse(inputs)

    part1_result = calculate_with_perimeter(parsed)
    print(f"Part 1 - Total price of fencing: {part1_result}")

    part2_result = calculate_with_corner(parsed)
    print(f"Part 2 - Total price of fencing: {part2_result}")


if __name__ == "__main__":
    main()
