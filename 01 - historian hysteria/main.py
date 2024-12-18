from collections import Counter

def sort_lists():
    """Sorts the lists into 2, separate, sorted lists"""
    left_list, right_list = read_file()
    left_list.sort()
    right_list.sort()
    return left_list, right_list

def find_distance(left_list, right_list):
    """Finds the total distance between the two lists"""
    total_distance = 0
    for left, right in zip(left_list, right_list):
        total_distance += abs(int(left) - int(right))
    return total_distance

def read_file():
    """Reads the file and returns the two lists"""
    left_list = []
    right_list = []
    with open("input.txt", "r") as file:
        for line in file:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))
    return left_list, right_list

def create_occurrences_dict():
    """Creates a dictionary of the # of times each number in the left list appears in the right list"""
    left_list, right_list = read_file()
    
    # count occurrences in the right list
    right_counts = Counter(right_list)
    return left_list, right_counts

def find_similarity_score(left_list, right_counts):
    """Finds the similarity score"""
    similarity_score = 0
    for number in left_list:
        similarity_score += number * right_counts[number]
    return similarity_score

def main():
    """Main function"""
    left_list, right_list = sort_lists()
    total_distance = find_distance(left_list, right_list)
    print('Total Distance: ', total_distance)
    left_list, right_counts = create_occurrences_dict()
    similarity_score = find_similarity_score(left_list, right_counts)
    print('Similarity Score: ', similarity_score)
    
if __name__ == "__main__":
    main()