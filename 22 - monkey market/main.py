def read_file():
    """Read input"""
    with open("input.txt", "r") as file:
        return [int(line.strip()) for line in file.readlines()]

def next_secret_number(secret_number):
    """
    Computes the next secret number in the sequence based on the given rules.
    """
    # multiply by 64, mix, and prune
    secret_number ^= (secret_number * 64)
    secret_number %= 16777216

    # divide by 32, mix, and prune
    secret_number ^= (secret_number // 32)
    secret_number %= 16777216

    # multiply by 2048, mix, and prune
    secret_number ^= (secret_number * 2048)
    secret_number %= 16777216

    return secret_number

def simulate_buyer(secret_number, steps):
    """
    Simulates the generation of `steps` secret numbers for a single buyer.
    Returns the final secret number after `steps` generations
    """
    for _ in range(steps):
        secret_number = next_secret_number(secret_number)
    return secret_number

def main():
    """Main function"""
    buyers = read_file()
    steps = 2000  # num steps to simulate for each buyer

    total = sum(simulate_buyer(buyer, steps) for buyer in buyers)

    print(f"The sum of the 2000th secret numbers is: {total}")

if __name__ == "__main__":
    main()
