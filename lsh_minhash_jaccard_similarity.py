import hashlib

# Function to generate shingles from a string
def generate_shingles(s, k):
    shingles = set()
    for i in range(len(s) - k + 1):
        shingle = s[i:i+k]
        shingles.add(shingle)
    return shingles


# Function to generate hash value using SHA-256
def hash_value(item):
    return int(hashlib.sha256(item.encode('utf-8')).hexdigest(), 16)


# Function to create MinHash signature for a set of items
def minhash_signature(items, num_hashes):
    minhash_values = []
    for i in range(num_hashes):
        hash_values = [hash_value(str(item) + str(i)) for item in items]
        minhash_values.append(min(hash_values))
    return minhash_values


# Function to calculate Jaccard similarity between two sets
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / float(union)


# Function to perform LSH and group similar sets together
def lsh_minhash_jaccard_similarity(strings, shingle_size=3, num_hashes=32, num_bands=32, threshold=0.75):
    duplicates = []
    candidate_pairs = set()
    bands = num_hashes // num_bands

    # Generate shingles for each string
    shingles_dict = {i: generate_shingles(s, shingle_size) for i, s in enumerate(strings)}

    # Check if any of the shingles are empty.
    # If yes, remove them from the dictionary
    for i, shingles in shingles_dict.items():
        if len(shingles) == 0:
            print(f"Empty shingles for string {i}")
            print(f'String: {strings[i-1]}')

    # Generate MinHash signatures for each set of shingles
    signatures = {i: minhash_signature(shingles, num_hashes) for i, shingles in shingles_dict.items()}

    # Perform LSH and identify potential duplicates
    for band in range(num_bands):
        bucket = {}
        for i, signature in signatures.items():
            band_signature = tuple(signature[band * bands: (band + 1) * bands])
            if band_signature in bucket:
                bucket[band_signature].append(i)
            else:
                bucket[band_signature] = [i]
        
        for _, similar_items in bucket.items():
            if len(similar_items) > 1:
                for i in range(len(similar_items)):
                    for j in range(i + 1, len(similar_items)):
                        candidate_pairs.add((similar_items[i], similar_items[j]))
    
    # Check Jaccard similarity for candidate pairs
    for pair in candidate_pairs:
        i, j = pair
        sim = jaccard_similarity(shingles_dict[i], shingles_dict[j])
        if sim >= threshold:
            duplicates.append((strings[i], strings[j], sim))

    return duplicates

if __name__ == "__main__":
    # strings = [
    #     "hello world",
    #     "hello there",
    #     "hi there",
    #     "python programming",
    #     "python coding",
    #     "coding in python",
    #     "data science",
    #     "machine learning",
    #     "deep learning",
    #     "data analysis",
    #     "hello woorld"
    # ]
    import json
    import time

    with open('texts.json', 'r') as f:
        strings = json.load(f)
        print(f'Length of input: {len(strings)}')
        time_start = time.time()
        duplicates = lsh_minhash_jaccard_similarity(strings)
        time_end = time.time()
        print(f'Time taken: {time_end - time_start:.2f} seconds\n')

        # Output duplicates
        for pair in duplicates:
            print(f'Similarity: {pair[2]:.2f}')
            print(f"Duplicate Pair: {pair[0]} | {pair[1]}")
            print('-' * 200)