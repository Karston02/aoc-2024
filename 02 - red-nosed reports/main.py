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