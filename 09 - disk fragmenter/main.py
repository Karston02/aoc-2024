def compact_disk(disk_map):
    # convert string to list of integers representing file lengths
    lengths = [int(x) for x in disk_map]
    
    # initial representation of disk
    disk = []
    for i, length in enumerate(lengths):
        disk.extend([i] * length)
    
    # find free positions
    free_positions = []
    for index, value in enumerate(disk):
        # a position free if it's empty ('.') or moved (-1)
        if value == '.' or value == -1:
            free_positions.append(index)
    
    # from right to left
    while free_positions:
        # find rightmost non-free block
        right_block_idx = len(disk) - 1
        while right_block_idx >= 0 and (disk[right_block_idx] == '.' or disk[right_block_idx] == -1):
            right_block_idx -= 1
        
        # if no non-free block found, break
        if right_block_idx < 0:
            break
        
        # find leftmost free space to move block to
        left_free_idx = min(free_positions)
        
        # Mmve the block
        disk[left_free_idx] = disk[right_block_idx]
        disk[right_block_idx] = -1  # Mark as moved
        
        # update free positions
        free_positions.remove(left_free_idx)
        free_positions.append(right_block_idx)
        free_positions.sort()
    
    # calculate checksum
    checksum = 0
    for position, block_id in enumerate(disk):
        # skip free space blocks (marked as -1 or '.')
        if block_id == -1 or block_id == '.':
            continue
        
        # multiply block position by its file ID
        block_value = position * block_id
        checksum += block_value
    
    return checksum

def main():
    """Main function"""

if __name__ == '__main__':
    main()