"""
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash,
you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her
with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual,
though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where
irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?


PART 2

The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?


"""

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
                (-1, 1), # ottom-left to top-right
            ]
            # check all 8 directions for XMAS
            for dx, dy in directions:
                if check_direction(x, y, dx, dy):
                    total_count += 1

    return total_count

def main():
    """Main function"""
    grid = read_file()
    print(count_xmas_occurrences(grid))


if __name__ == "__main__":
    main()
