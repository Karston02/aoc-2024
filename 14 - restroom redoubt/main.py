def read_file():
    """Read input"""
    with open("input.txt", "r") as file:
        return file.readlines()

def parse_input(lines):
    """Parse the input lines into a list of robots"""
    robots = []
    for line in lines:
        line = line.strip()
        # parse the position and velocity of each robot
        pos_part, vel_part = line.split(" ")
        px, py = map(int, pos_part[2:].split(","))
        vx, vy = map(int, vel_part[2:].split(","))
        robots.append(((px, py), (vx, vy)))
    return robots

def simulate_robots(robots, width, height, seconds):
    """Simulate the robots after the given seconds"""
    positions = []
    for (px, py), (vx, vy) in robots:
        # calculate new position after given seconds, applying wrap-around
        new_x = (px + vx * seconds) % width
        new_y = (py + vy * seconds) % height
        positions.append((new_x, new_y))
    return positions

def count_robots_in_quadrants(positions, width, height):
    """Count the number of robots in each quadrant"""
    mid_x, mid_y = width // 2, height // 2

    quadrant_counts = [0, 0, 0, 0]  # Q1, Q2, Q3, Q4
    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue  # ignore robots exactly in the middle

        if x < mid_x and y < mid_y:
            quadrant_counts[1] += 1  # Q2
        elif x < mid_x and y > mid_y:
            quadrant_counts[2] += 1  # Q3
        elif x > mid_x and y < mid_y:
            quadrant_counts[0] += 1  # Q1
        elif x > mid_x and y > mid_y:
            quadrant_counts[3] += 1  # Q4

    return quadrant_counts

def calculate_safety_factor(robots, width, height, seconds):
    """Calculate the safety factor of the robots after the given seconds"""
    positions = simulate_robots(robots, width, height, seconds)
    quadrant_counts = count_robots_in_quadrants(positions, width, height)
    safety_factor = 1
    for count in quadrant_counts:
        safety_factor *= count
    return safety_factor

def main():
    """Main function"""
    width, height = 101, 103
    seconds = 100

    lines = read_file()
    robots = parse_input(lines)

    safety_factor = calculate_safety_factor(robots, width, height, seconds)
    print("Safety Factor:", safety_factor)

if __name__ == "__main__":
    main()
