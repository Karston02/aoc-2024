from collections import Counter

def read_file():
    """Reads input"""
    with open("input.txt", 'r') as file:
        return list(map(int, file.read().strip().split()))

def process_stone(stone):
    """Processes a stone according to rules and returns the resulting stones"""
    stone_str = str(stone)
    # if stone 0, return 1
    if stone == 0:
        return [1]
    elif len(stone_str) % 2 == 0:
        # split the stone in half and return the two halves
        mid = len(stone_str) // 2
        left = int(stone_str[:mid])
        right = int(stone_str[mid:])
        return [left, right]
    else:
        # if the stone is odd, return the stone multiplied by 2024
        return [stone * 2024]

def blink(stones):
    """Processes all stones during a single blink, accounting for duplicate values"""
    new_stones = Counter()
    # process each stone and add the resulting stones to the new_stones counter
    for stone, count in stones.items():
        for new_stone in process_stone(stone):
            new_stones[new_stone] += count
    return new_stones

def count_stones_after_blinks(blinks):
    """Reads the input, processes the stones for the given blinks, and returns the total number of stones"""
    initial_stones = read_file()
    stones = Counter(initial_stones)
    for _ in range(blinks):
        stones = blink(stones)
    return sum(stones.values())

def main():

    blinks_25 = 25
    result_25 = count_stones_after_blinks(blinks_25)
    print(f"Number of stones after {blinks_25} blinks: {result_25}")

    blinks_75 = 75
    result_75 = count_stones_after_blinks(blinks_75)
    print(f"Number of stones after {blinks_75} blinks: {result_75}")

if __name__ == "__main__":
    main()

