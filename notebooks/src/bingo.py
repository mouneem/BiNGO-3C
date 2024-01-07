
def dict_to_fasta(dict,path='./data/1 - simulated_dataset/'):
    file=open(path+'simulated_dataset.fasta','w+')
    for id in dict:
        sequence=dict[id]
        file.write('>'+str(id)+'\n')
        file.write(sequence.replace('\n','')+'\n')


# Reads a FASTA file and returns a dictionary of sequences.
def dict_of_seqs_from_fasta_file(file_path, header_cleaning=None, seq_case='upper', include_empty=False):
    """
    Parameters:
    - file_path (str): Path to the FASTA file.
    - header_cleaning (function, optional): A function to process the headers (e.g., removing unwanted characters).
    - seq_case (str, 'upper' or 'lower'): Whether to convert sequences to uppercase ('upper') or lowercase ('lower').
    - include_empty (bool): Whether to include sequences that are empty.

    Returns:
    - dict: A dictionary with headers as keys and sequences as values.
    """
    sequences = {}

    with open(file_path, 'r') as fasta_file:
        current_header = None
        current_sequence = []

        for line in fasta_file:
            line = line.strip()
            if line.startswith('>'):  # Header line
                if current_header and (include_empty or current_sequence):
                    sequences[current_header] = ''.join(current_sequence).upper() if seq_case == 'upper' else ''.join(current_sequence).lower()
                current_header = header_cleaning(line[1:]) if header_cleaning else line[1:]
                current_sequence = []
            else:  # Sequence line
                current_sequence.append(line)

        # Adding the last sequence
        if current_header and (include_empty or current_sequence):
            sequences[current_header] = ''.join(current_sequence).upper() if seq_case == 'upper' else ''.join(current_sequence).lower()

    return sequences


import random

# Generates a random DNA sequence of length n.
def random_delimiter(n=11):
    """
    - n (int, optional): The length of the DNA sequence. Defaults to 11.
    """
    bases = "ATGC"
    return ''.join(random.choice(bases) for _ in range(n))


import sys

# Processes a DNA sequence, replaces each nucleotide with binary representation,
def binarize(sequence, convert_dicimal = True , verbose=False):
    """
    - sequence (str): The DNA sequence to process.
    - verbose (bool): If True, prints memory sizes at each step.
    """
    mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
    try:

        # Replace each base with binary representation
        binary_sequence = ''.join(mapping[base] for base in sequence)


        # Convert string to actual binary type (bytes)
        binary_data = int(binary_sequence, 2).to_bytes((len(binary_sequence) + 7) // 8, byteorder='big')
        result = binary_data
        if convert_dicimal:
            # Convert to decimal digit
            decimal_digit = int(binary_sequence, 2)
            result = decimal_digit

        # Print size of decimal digit if verbose is True
        if verbose:
            original_size = sys.getsizeof(sequence)
            print(f"Original Sequence Size: {original_size} bytes")
            replaced_size = sys.getsizeof(binary_sequence)
            print(f"Size After Replacement: {replaced_size} bytes")
            binary_data_size = sys.getsizeof(binary_data)
            print(f"Binary Data Size: {binary_data_size} bytes")
            if convert_dicimal:
                decimal_size = sys.getsizeof(decimal_digit)
                print(f"Decimal Digit Size: {decimal_size} bytes")
        return result
    except:
        return 0





# input: list of sub-sequences
# output: list of binary values
def binarize_a_list(lst, verbose = False, convert_dicimal = True):
    return [ binarize(e, convert_dicimal, verbose) for e in lst]


import re
from multiprocessing import Pool

# Worker function to generate words for a segment of the sequence.
def generate_words_worker(args):
    sequence_segment, word_size, skip_chars = args
    words = []
    i = 0

    while i < len(sequence_segment):
        word = sequence_segment[i:i + word_size]
        word = word.upper()
        word = re.sub(r'[^ATGC]', '', word)
        words.append(word)
        i += word_size + skip_chars

    return words

# Divides a sequence into words of a specified size, with a defined number of characters skipped in between.
def generate_words_from_Seq(sequence, s=11, w=3, verbose=False, n_parallel=1):
    """
    Parameters:
    - sequence (str): The input sequence to be divided.
    - s (int): The size of each word (number of characters in each word).
    - w (int): The number of characters to skip between words.
    - verbose (bool): If True, prints the number of words generated.
    - n_parallel (int): The number of parallel processes to use.

    Returns: A list of words extracted from the sequence.
    """
    if n_parallel > 1:
        # Split the sequence into chunks for parallel processing
        chunk_size = len(sequence) // n_parallel
        sequence_chunks = [sequence[i:i + chunk_size] for i in range(0, len(sequence), chunk_size)]

        # Create a pool of workers and process the chunks
        with Pool(n_parallel) as pool:
            results = pool.map(generate_words_worker, [(chunk, s, w) for chunk in sequence_chunks])

        # Flatten the list of words from all chunks
        words = [word for sublist in results for word in sublist]
    else:
        # Process the sequence in a single thread
        words = generate_words_worker((sequence, s, w))
    # Print the number of words if verbose is True
    if verbose:
        print(f"Number of words generated: {len(words)}")


    return words




def process_sequences(args):
    """
    Processes a list of sequences, dividing each into words and optionally converting to binary.
    """
    sequences, word_size, skip_chars, convert_to_binary = args
    all_words = set()

    for sequence in sequences:
        try:
            words = generate_words_from_Seq(sequence, word_size, skip_chars)
        except:
            pass

        if convert_to_binary:
            words = set(binarize_a_list(words) )
        else:
            words = set(words)

        all_words.update(words)

    return list(all_words)

def generate_words_from_dictSeq(dictSeq, s=11, w=3, verbose=False, n_parallel=0, convert_to_binary=False):
    """
    Processes a dictionary of lists of sequences, dividing each sequence into words and optionally converting to binary.

    Parameters:
    - dictSeq (dict of lists): Dictionary of lists of sequences.
    - s (int): Size of each word.
    - w (int): Number of characters to skip between words.
    - verbose (bool): If True, prints additional information.
    - n_parallel (int): Number of parallel processes to use.
    - convert_to_binary (bool): If True, converts words to binary representation.

    Returns:
    - dict: Dictionary of lists of words (or binary representations) extracted from sequences.
    """
    if n_parallel > 1:
        with Pool(n_parallel) as pool:
            results = pool.map(process_sequences, [(sequences, s, w, convert_to_binary) for sequences in dictSeq.values()])
        words_dict = dict(zip(dictSeq.keys(), results))
    else:
        words_dict = {key: process_sequences((sequences, s, w, convert_to_binary)) for key, sequences in dictSeq.items()}

    if verbose:
        for key, words in words_dict.items():
            print(f"Key: {key}, Number of words: {len(words)}")

    return words_dict






def dictSubSeq_from_dictSeq(dictSeq, delimiter, verbose=False):
    """
    Splits sequences in a dictionary into subsequences based on a specified delimiter.

    Parameters:
    - dictSeq (dict): A dictionary with sequences.
    - delimiter (str): The delimiter used to split the sequences.

    Returns:
    - dict: A dictionary with subsequences as values, split based on the delimiter.

    Prints the count of delimiter occurrences in each original sequence.
    """
    subseq_dict = {}
    for key, sequence in dictSeq.items():
        # Count occurrences of the delimiter
        delimiter_count = sequence.count(delimiter)
        if verbose:
            # Print the count of the delimiter in the current sequence
            print(f"Delimiter '{delimiter}' found {delimiter_count} times in sequence with key '{key}'.")

        # Split the sequence and store in the new dictionary
        subseq_dict[key] = sequence.split(delimiter)

    return subseq_dict

def jaccard_score(list1, list2):
    """Computes the Jaccard score between two lists."""
    set1, set2 = set(list1), set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


from itertools import combinations
from multiprocessing import Pool

def process_pair(pair):
    """Processes a pair of lists and computes their Jaccard score."""
    key1, list1, key2, list2 = pair
    score = jaccard_score(list1, list2)
    return (key1, key2, score)

def compute_jaccard_scores(dictSeq, n_parallel=0):
    """
    Computes Jaccard scores for all pairs of sequences in the input dictionary.

    Parameters:
    - dictSeq (dict): Dictionary of lists of numeric values.
    - n_parallel (int): Number of parallel processes to use.

    Returns:
    - dict: Dictionary of Jaccard scores for each pair of keys in dictSeq.
    """
    pairs = [(key1, dictSeq[key1], key2, dictSeq[key2]) for key1, key2 in combinations(dictSeq.keys(), 2)]
    
    if n_parallel > 1:
        with Pool(n_parallel) as pool:
            results = pool.map(process_pair, pairs)
    else:
        results = map(process_pair, pairs)

    scores = {(key1, key2): score for key1, key2, score in results}
    return scores
import os

def get_max_cores():
    """
    Returns the maximum number of CPU cores available on the current machine.

    Returns:
    - int: Number of available CPU cores.
    """
    return os.cpu_count()


import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy


import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

# Plots a dendrogram based on the computed Jaccard scores.
def plot_dendrogram(scores, labels=None, method='average', metric='euclidean', show=True, figsize = [10,8], color_threshold = False, title = 'Dendrogram'):
    """
    Parameters:
    - scores (dict): Dictionary of Jaccard scores, where keys are tuples of pair names.
    - labels (list, optional): List of labels for the dendrogram. If None, pair names from scores are used.
    - method (str): Linkage method for hierarchical clustering (e.g., 'single', 'complete', 'average', 'ward').
    - metric (str): Metric used for distance (e.g., 'euclidean', 'cityblock'). Only used if scores are not provided.
    - show (bool): If True, shows the plot, otherwise returns the figure object.
    """
    if labels is None:
        labels = list(set(key for pair in scores.keys() for key in pair))
    matrix = np.ones((len(labels), len(labels)))

    for (i, label1), (j, label2) in combinations(enumerate(labels), 2):
        score = scores.get((label1, label2)) or scores.get((label2, label1))
        if score is not None:
            distance = 1 - score  # Convert similarity score to distance
            matrix[i, j] = matrix[j, i] = distance

    # Convert the distance matrix to a condensed form required by linkage
    condensed_matrix = squareform(matrix)

    # Perform hierarchical clustering
    Z = linkage(condensed_matrix, method=method, metric=metric)

    # Plotting the dendrogram
    fig = plt.figure(figsize=figsize)
    if color_threshold:
        dendrogram(Z, labels=labels, color_threshold= color_threshold)
    else:
        dendrogram(Z, labels=labels)

    plt.title(title)
    plt.xlabel('Sequence')
    plt.ylabel('Distance')

    if show:
        plt.show()
    else:
        return fig
    

import numpy as np  
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations

def scores_to_matrix(scores, labels = None):
    """
    Converts a dictionary of Jaccard scores to a square matrix.

    Parameters:
    - scores (dict): Dictionary of Jaccard scores, where keys are tuples of pair names.
    - labels (list): List of labels corresponding to the matrix's rows and columns.

    Returns:
    - 2D numpy array: Square matrix of scores.
    """
    matrix = np.ones((len(labels), len(labels)))

    for (i, label1), (j, label2) in combinations(enumerate(labels), 2):
        score = scores.get((label1, label2)) or scores.get((label2, label1))
        if score is not None:
            matrix[i, j] = matrix[j, i] = score

    return matrix

def plot_clustermap(scores, labels=None, method='average', metric='euclidean', cmap='vlag', figsize=(10, 10), show=True, title = ''):
    """
    Plots a clustermap of the provided Jaccard scores.

    Parameters:
    - scores (dict): Dictionary of Jaccard scores, where keys are tuples of pair names.
    - labels (list, optional): Labels for the rows and columns of the heatmap. If None, pair names from scores are used.
    - method (str): Linkage method for hierarchical clustering (e.g., 'single', 'complete', 'average', 'ward').
    - metric (str): Metric used for distance (e.g., 'euclidean', 'cityblock').
    - cmap (str): Colormap for the heatmap.
    - figsize (tuple): Size of the figure.
    - show (bool): If True, shows the plot, otherwise returns the figure object.

    Returns:
    - If show is False, returns the figure object. Otherwise, displays the clustermap.
    """
    if labels is None:
        labels = list(set(key for pair in scores.keys() for key in pair))

    # Convert scores to a similarity matrix
    similarity_matrix = scores_to_matrix(scores, labels)

    # Create and plot the clustermap
    sns.set(style="white")
    g = sns.clustermap(similarity_matrix, method=method, metric=metric, cmap=cmap, figsize=figsize, xticklabels=labels, yticklabels=labels)
    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90)
    plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0)



    # Extract the linkage matrices
    row_linkage = g.dendrogram_row.linkage

    # Plot the row dendrogram
    plt.figure(figsize=figsize)
    d = dendrogram(row_linkage, labels=labels)
    plt.xticks(rotation=90)  # Rotate column labels by 90 degrees
    plt.show()

    if show:
        plt.show()
    else:
        return g
    
