from sys import maxsize
from itertools import pairwise, permutations

# lookup tables for direction and numpad
dir_base_lookup = {
    ('A', 'A'): 'A', ('^', '^'): 'A', ('>', '>'): 'A', ('v', 'v'): 'A', ('<', '<'): 'A',
    ('A', '^'): '<A', ('^', 'A'): '>A', ('A', '>'): 'vA', ('>', 'A'): '^A', ('v', '^'): '^A',
    ('^', 'v'): 'vA', ('v', '<'): '<A', ('<', 'v'): '>A', ('v', '>'): '>A', ('>', 'v'): '<A',
    ('A', 'v'): 'v<A', ('v', 'A'): '>^A', ('A', '<'): 'v<<A', ('<', 'A'): '>>^A',
    ('>', '<'): '<<A', ('<', '>'): '>>A', ('<', '^'): '>^A', ('^', '<'): 'v<A', ('>', '^'): '<^A', 
    ('^', '>'): 'v>A'
}

dirs = [
    [('^', -1), ('v', 1)],
    [('<', -1), ('>', 1)],
]

numpad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [' ', '0', 'A']
]

numpad_lookup = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
    ' ': (3, 0), '0': (3, 1), 'A': (3, 2),
}

dirpad = [
    [' ', '^', 'A'],
    ['<', 'v', '>'],
]

dirpad_lookup = {
    ' ': (0, 0), '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}

# memo dicts
memo_dir = {}
memo_num = {}

def dir_dfs(key_start, key_end, depth=0):
    """Solve the shortest path between two keys in dirpad"""
    if depth == 0:
        return dir_base_lookup[key_start, key_end]

    s = dir_dfs(key_start, key_end, depth-1)
    out = "".join(dir_base_lookup[k0, k1] for k0, k1 in pairwise('A' + s))
    return out

def compute_move(y0, x0, y1, x1):
    """Compute the shortest path between two keys in numpad"""
    y_dist, x_dist = y1 - y0, x1 - x0
    y_key, _ = dirs[0][y_dist > 0]
    x_key, _ = dirs[1][x_dist > 0]

    start_move = ""
    if (y0 == 3 or y1 == 3) and (x0 == 0 or x1 == 0):
        if x0 == 0:
            start_move = '>'
            mov_s = y_key * abs(y_dist) + x_key * (abs(x_dist) - 1)
        else:
            start_move = '^'
            mov_s = y_key * (abs(y_dist) - 1) + x_key * abs(x_dist)
    else:
        mov_s = y_key * abs(y_dist) + x_key * abs(x_dist)

    return start_move, mov_s

def num_solve(key_start, key_end):
    """Solve the shortest path between two keys in numpad"""
    y0, x0 = numpad_lookup[key_start]
    y1, x1 = numpad_lookup[key_end]

    start_move, mov_s = compute_move(y0, x0, y1, x1)
    possible_inputs = [
        'A' + start_move + ''.join(x) + 'A'
        for x in set(permutations(mov_s))
    ]

    min_score, min_inputs = maxsize, ""
    for inputs in possible_inputs:
        sequence = ''.join(dir_dfs(k0, k1, depth=1) for k0, k1 in pairwise(inputs))
        if len(sequence) < min_score:
            min_score = len(sequence)
            min_inputs = sequence
    
    memo_num[key_start, key_end] = min_score
    return min_inputs

# Function to calculate the final score
def calculate_score(codes):
    out = 0
    for code in codes:
        m = int(code[:-1])
        s = ''.join(num_solve(a, b) for a, b in pairwise("A" + code))
        out += len(s) * m
    return out

if __name__ == "__main__":
    # Read input and compute result
    with open("input.txt") as file:
        codes = file.read().splitlines()

    result = calculate_score(codes)
    print("Score:", result)
