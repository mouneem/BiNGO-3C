# BiNGO-3C: Binary Encoding of Genomic Sequences for Optimal Compression, Comparison and Clustering.

## Abstract
The vast amount of data generated by sequencing technologies gave rise to the need for faster and adequate algorithms. Statistical comparison methods for the comparison of biological sequences based on word-counts such as k-mer have shown great potential. However the characters-string-based representation of DNA and the redundancy of common words leave much to be desired, in terms of memory and complexity optimization. Here, we explore the potential optimization of the classic alignment-free sliding-window for sequence comparison by introducing a new representation of DNA sequences for optimal time and memory consumption. 

To reduce the memory and time consumption in our approach, we start by splitting the long DNA sequence into smaller words of size s and a gap h, as in any other sliding-window algorithm.  We then change the representation of the words from DNA bases (A, C, G and T) to a 2-bit binary format (00, 01, 10 and 11) respectively, then to the numeric value corresponding to the resulting binary string. This step significantly reduces the storage-memory as well as the computation time for the next steps. Finally the set of numeric values are compared to each other and clustered using Jaccard-Similarity Index to compute a similarity score.


