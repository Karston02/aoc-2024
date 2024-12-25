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

def calculate_checksum(blocks):
    """Calculate the filesystem checksum"""
    checksum = 0
    for pos, block in enumerate(blocks):
        if block != '.':
            checksum += pos * block
    return checksum

def solve_disk_compaction(disk_map):
    """Solve the disk compaction problem"""
    # parse the disk map into blocks
    blocks = parse_disk_map(disk_map)
    
    # compact the disk
    compacted_blocks = compact_disk(blocks)
    
    # calculate and return checksum
    return calculate_checksum(compacted_blocks)

def main():
    """Main function"""
    disk_map = read_file()
    result = solve_disk_compaction(disk_map)
    print(f"The filesystem checksum after compaction is: {result}")

if __name__ == "__main__":
    main()