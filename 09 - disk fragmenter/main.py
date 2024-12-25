def read_file():
    """Read input"""
    with open('input.txt', 'r') as file:
        return file.read().strip()

def parse_disk_map(disk_map):
    """Convert the disk map string into a list of blocks with file IDs"""
    # separate into alternating file sizes and free space sizes
    sizes = [int(x) for x in disk_map]
    
    # convert to actual blocks representation
    blocks = []
    file_id = 0
    for i, size in enumerate(sizes):
        if i % 2 == 0:  # file blocks
            blocks.extend([file_id] * size)
            file_id += 1
        else:  # free space blocks
            blocks.extend(['.'] * size)
    return blocks

def compact_disk(blocks):
    """Compact the disk by moving files from right to left"""
    # make a copy so we dont change original
    blocks = blocks.copy()
    n = len(blocks)
    
    while True:
        # find rightmost file
        right_pos = n - 1
        while right_pos >= 0 and blocks[right_pos] == '.':
            right_pos -= 1
        
        if right_pos < 0:
            break
            
        # find leftmost free space
        left_pos = 0
        while left_pos < n and blocks[left_pos] != '.':
            left_pos += 1
            
        if left_pos >= right_pos:
            break
            
        # move the file block
        blocks[left_pos] = blocks[right_pos]
        blocks[right_pos] = '.'
    
    return blocks

def find_file_info(blocks, file_id):
    """Find start position and size of a file"""
    start = None
    size = 0
    for i, block in enumerate(blocks):
        if block == file_id:
            if start is None:
                start = i
            size += 1
    return start, size

def find_leftmost_space(blocks, start_pos, required_size):
    """Find the leftmost contiguous free space that can fit the file"""
    current_size = 0
    start = None
    
    # linear search
    for i in range(start_pos):
        if blocks[i] == '.':
            if start is None:
                start = i
            current_size += 1
            if current_size == required_size:
                return start
        else:
            start = None
            current_size = 0
            
    return None

def move_file(blocks, file_id):
    """Move a single file to the leftmost possible position"""
    # find the file's current position and size
    start, size = find_file_info(blocks, file_id)
    if start is None:
        return blocks
    
    # find leftmost space that can fit the file
    new_start = find_leftmost_space(blocks, start, size)
    if new_start is None:
        return blocks
    
    new_blocks = blocks.copy()
    # clear old position
    for i in range(start, start + size):
        new_blocks[i] = '.'
    # place in new position
    for i in range(new_start, new_start + size):
        new_blocks[i] = file_id
        
    return new_blocks

def compact_disk_whole_files(blocks):
    """Compact the disk by moving whole files from right to left"""
    # find the highest file ID
    max_file_id = max(block for block in blocks if block != '.')
    
    # process files in decreasing order of file ID
    for file_id in range(max_file_id, -1, -1):
        blocks = move_file(blocks, file_id)
    
    return blocks

def calculate_checksum(blocks):
    """Calculate the filesystem checksum"""
    checksum = 0
    for pos, block in enumerate(blocks):
        if block != '.':
            checksum += pos * block
    return checksum

def solve_disk_compaction_part1(disk_map):
    """Solve part 1 of the disk compaction problem"""
    blocks = parse_disk_map(disk_map)
    compacted_blocks = compact_disk(blocks)
    return calculate_checksum(compacted_blocks)

def solve_disk_compaction_part2(disk_map):
    """Solve part 2 of the disk compaction problem"""
    blocks = parse_disk_map(disk_map)
    compacted_blocks = compact_disk_whole_files(blocks)
    return calculate_checksum(compacted_blocks)

def main():
    """Main function"""
    disk_map = read_file()
    
    result1 = solve_disk_compaction_part1(disk_map)
    result2 = solve_disk_compaction_part2(disk_map)
    
    print(f"Part 1 - The filesystem checksum after block-by-block compaction is: {result1}")
    print(f"Part 2 - The filesystem checksum after whole-file compaction is: {result2}")

if __name__ == "__main__":
    main()