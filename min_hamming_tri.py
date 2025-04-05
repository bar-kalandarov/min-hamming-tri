import numpy as np
from collections import defaultdict
import argparse
import math


def calculate_hamming_distance(vec1: list[int], vec2: list[int]) -> int:
    """
    Calculates the Hamming distance between two binary vectors.

    The Hamming distance is the number of positions where the corresponding elements of two vectors differ.

    Args:
        vec1 (list[int]): The first binary vector.
        vec2 (list[int]): The second binary vector.

    Returns:
        int: The Hamming distance between the two vectors.

    Raises:
        ValueError: If the input vectors have different lengths.
    """

    if len(vec1) != len(vec2):
        raise ValueError("Input vectors must have the same length.")

    return sum(b1 != b2 for b1, b2 in zip(vec1, vec2))


def compute_min_hamming(vectors, curr_min):
    """
    Computes the minimum Hamming distance between vectors in a given list, while also counting
    how many pairs of vectors are skipped based on the triangular inequality property.

    The function uses the first vector to compute the Hamming distances to all other vectors and
    checks pairs of vectors using the triangular inequality to skip unnecessary calculations.

    Args:
        vectors (list[list[int]]): A list of binary vectors to compare.
        curr_min (int): The current minimum Hamming distance from previous computations.

    Returns:
        tuple: A tuple containing three values:
            - The minimum Hamming distance found (`min_hamming`).
            - The total number of pairs that were compared (`total_pairs`).
            - The total number of pairs that were skipped based on the triangular inequality (`skipped_pairs`).
    """

    # Check if the list of vectors is empty or contains fewer than 2 vectors.
    if not vectors or len(vectors) < 2:
        return float('inf'), 0, 0

    first_vector = vectors[0]
    num_of_vectors = len(vectors)
    min_hamming = curr_min

    skipped_pairs = 0
    total_pairs = 0

    # Compute the Hamming distances from the first vector to all other vectors.
    first_distances = []
    for i in range(1, num_of_vectors):
        total_pairs += 1
        hamming_distance = calculate_hamming_distance(first_vector, vectors[i])
        first_distances.append(hamming_distance)

        min_hamming = min(min_hamming, hamming_distance)

    # Compute the Hamming distances for all other pairs of vectors.
    for i in range(1, num_of_vectors):
        for j in range(i + 1, num_of_vectors):
            total_pairs += 1

            # Calculate the "low bar" using the triangular inequality.
            low_bar = max(first_distances[i - 1] - first_distances[j - 1],
                          first_distances[j - 1] - first_distances[i - 1])

            # If the "low bar" is greater than the current minimum, skip this pair.
            if low_bar > min_hamming:
                skipped_pairs += 1
                continue

            hamming_distance = calculate_hamming_distance(vectors[i], vectors[j])

            min_hamming = min(min_hamming, hamming_distance)

    return min_hamming, total_pairs, skipped_pairs


def classify_vectors_by_random_bits(vectors: list[list[int]], num_of_bits: int) -> list[list[list[int]]]:
    """
    Classifies vectors into groups based on randomly selected bit positions.

    Each vector is assigned to a group determined by the values at randomly chosen indices.
    The function assumes that all vectors have the same length.

    Args:
        vectors (list[list[int]]): A list of binary vectors of equal length.
        num_of_bits (int): The number of random bit positions to use for classification.

    Returns:
        list[list[list[int]]]: A list of groups, where each group contains vectors
        that share the same values at the selected bit positions.
    """

    if not vectors:
        return []

    vector_length = len(vectors[0])
    indices = np.random.choice(vector_length, num_of_bits, replace=False)
    groups = defaultdict(list)

    for vec in vectors:
        key = tuple(vec[i] for i in indices)
        groups[key].append(vec)

    return list(groups.values())


def analyze_hamming_groups(groups, curr_min):
    """
    Analyzes the Hamming distances within groups of vectors by computing the minimum Hamming distance
    for each group and tracking the total number of comparisons made and the number of skipped comparisons
    based on the triangular inequality.

    The function iterates over each group, calls `compute_min_hamming` for each, and updates the overall
    minimum Hamming distance, as well as the counts of total and skipped comparisons.

    Args:
        groups (list[list[list[int]]]): A list of groups, where each group is a list of binary vectors
                                         to be compared.
        curr_min (int): The current minimum Hamming distance from previous computations.

    Returns:
        tuple: A tuple containing two values:
            - The total number of pairs of vectors compared across all groups (`total_count`).
            - The total number of skipped comparisons based on the triangular inequality (`skipped_count`).
    """

    # Initialize overall minimum Hamming distance and counters for comparisons.
    min_hamming_overall = curr_min
    total_count = 0
    skipped_count = 0

    # Iterate through each group of vectors.
    for group in groups:
        min_hamming, total_pairs, skipped_pairs = compute_min_hamming(group, min_hamming_overall)

        min_hamming_overall = min(min_hamming_overall, min_hamming)

        skipped_count += skipped_pairs
        total_count += total_pairs

    return min_hamming_overall, total_count, skipped_count


def main():
    """
    Main function to calculate the percentage of skipped Hamming distance comparisons
    between binary vectors using Locality Sensitive Hashing (LSH).

    The function generates random binary vectors, classifies them using LSH, and analyzes the
    Hamming distances between the vectors in multiple iterations. The result is the percentage
    of pairs of vectors that were skipped based on the triangular inequality property.

    The number of skipped and total comparisons are calculated across all iterations and reported.

    Command-line arguments:
        --vectors (int): The number of binary vectors to generate.
        --length (int): The length of each binary vector.
        --samples (int): The number of different inputs to compare.
        --iterations (int): The number of LSH iterations to perform.

    Returns:
        None (prints the percentage of skipped pairs).
    """

    parser = argparse.ArgumentParser(description="Evaluate triangle inequality improvement.")
    parser.add_argument("--vectors", type=int, required=True, help="Number of binary vectors")
    parser.add_argument("--length", type=int, required=True, help="Length of each binary vector")
    parser.add_argument("--samples", type=int, required=True, help="Number of case studies to check")
    parser.add_argument("--iterations", type=int, required=True, help="Number of LSH iterations")
    args = parser.parse_args()

    skipped = 0
    total = 0
    min_distance = args.length + 1

    # Set the number of indices to use in the LSH hash function to log(m/log(m))
    num_of_lsh_bits = round(math.log2(args.vectors / math.log2(args.vectors)))

    # Compare Iterations
    for _ in range(args.samples):
        binary_vectors = [np.random.randint(0, 2, args.length).tolist() for _ in range(args.vectors)]

        for _ in range(args.iterations):
            res = analyze_hamming_groups(classify_vectors_by_random_bits(binary_vectors, num_of_lsh_bits), min_distance)
            total += res[1]
            skipped += res[2]
            min_distance = min(min_distance, res[0])

    percentage_of_skipped = skipped / total * 100
    print(f"Skipped pairs rate is {percentage_of_skipped:.2f}%")


if __name__ == "__main__":
    main()

