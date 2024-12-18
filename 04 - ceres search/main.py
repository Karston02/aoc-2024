def read_file():
    """Reads input text file"""
    with open("input.txt") as f:
        return f.read().strip().splitlines()

def count_xmas_occurrences(grid):
    """Count occurrences of XMAS in the grid in all possible directions"""
    word = "XMAS"
    word_len = len(word)
    total_count = 0
    rows = len(grid)
    cols = len(grid[0])

    def check_direction(x, y, dx, dy):
        """Check if 'XMAS' is in a specific direction starting from (x, y)"""
        for i in range(word_len):
            # calculate next position in the grid
            next_x = x + i * dx
            next_y = y + i * dy

            # check if next position is out of bounds
            if not (0 <= next_x < rows and 0 <= next_y < cols):
                return False

            # check if the character at the current position matches the expected character in in XMAS
            if grid[next_x][next_y] != word[i]:
                return False

        # all chars match, true
        return True

    for x in range(rows):
        for y in range(cols):
            # Check in all 8 directions
            directions = [
                (0, 1),  # left to right
                (0, -1), # right to left
                (1, 0),  # top to bottom
                (-1, 0), # bottom to top
                (1, 1),  # top-left to bottom-right
                (-1, -1),# bottom-right to top-left
                (1, -1), # top-right to bottom-left
                (-1, 1), # bottom-left to top-right
            ]
            # check all 8 directions for XMAS
            for dx, dy in directions:
                if check_direction(x, y, dx, dy):
                    total_count += 1

    return total_count

def read_file():
    """Reads input text file"""
    with open("input.txt") as f:
        return f.read().strip().splitlines()

def count_mas_in_x(grid):
    """Count occurrences of X-MAS in the grid"""
    rows = len(grid)
    cols = len(grid[0])
    total_count = 0

    def is_x_mas(x, y):
        """Check if (x, y) is the center of an X-MAS pattern"""
        try:
            # ASCII checks for diagonals
            diag1 = ord(grid[x - 1][y - 1]) + ord(grid[x + 1][y + 1])  # top-left to bottom-right
            diag2 = ord(grid[x - 1][y + 1]) + ord(grid[x + 1][y - 1])  # top-right to bottom-left
            
            # ensure both diagonals sum to M + S (don't care about order)
            return (
                grid[x][y] == 'A'  # center must be A
                and diag1 == ord('M') + ord('S')  # diagonal 1 correct
                and diag2 == ord('M') + ord('S')  # diagonal 2 correct
            )
        except IndexError:
            return False  # out of bounds, not possible

    # traverse the grid and count valid patterns
    for x in range(1, rows - 1):  # avoid edges
        for y in range(1, cols - 1):  # avoid edges
            if is_x_mas(x, y):
                total_count += 1

    return total_count

def main():
    """Main function"""
    grid = read_file()
    print("Crossword Pattern: ", count_xmas_occurrences(grid))
    print("XMAS Patterns: ", count_mas_in_x(grid))


if __name__ == "__main__":
    main()
