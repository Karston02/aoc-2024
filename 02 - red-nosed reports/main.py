"""
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers
there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular
synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from
the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into
groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called
levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9

This example data contains six reports (rows) each containing five levels (columns).

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels
that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?


PART 2

The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise
be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts
as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?

"""

def is_safe(levels):
    """Determines if the levels are safe"""

    # by definition, safe
    if len(levels) < 2:
        return True

    trend = None  # tracks the trend: "increasing", "decreasing", or None

    for i in range(1, len(levels)):
        diff = levels[i] - levels[i-1]

        # check for invalid difference (can't be safe)
        if abs(diff) > 3 or diff == 0:
            return False

        # determine trend
        if diff > 0:  # increasing
            if trend == "decreasing": # change in trend
                return False
            trend = "increasing"
        elif diff < 0:  # decreasing
            if trend == "increasing": # change in trend
                return False
            trend = "decreasing"

    return True

def is_safe_with_dampener(levels):
    """Checks if the levels are safe with the dampener. Basically, it removes the
    i element from the list and checks if it would be safe without it"""
    for i in range(len(levels)):
        # safe from up until i, and from i+1 to the end
        if is_safe(levels[:i] + levels[i+1:]):
            return True
    return False

def main():
    """Main function"""
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        total = 0
        for line in lines:
            levels = list(map(int, line.strip().split()))
            if is_safe(levels):
                total += 1
        print('Total safe: ', total)
        
        dampener_total = 0
        for line in lines:
            levels = list(map(int, line.strip().split()))
            if is_safe_with_dampener(levels):
                dampener_total += 1
        print('Total safe with dampener: ', dampener_total)

if __name__ == '__main__':
    main()