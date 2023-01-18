# FSWM

The program takes a set of genomic sequences as input and generates a distance matrix with the pairwise distances between the input sequences.

Usage:
to compile type: make

run with: ./fswm [options] <sequences >

<sequence> format:

The input sequences must be contained in one single file FASTA format. Each species/genome must be represented by one single sequence in the input FASTA file. If you have multiple reads, contigs or chromosomes per input species, please concatenate them to one single sequence to make sure each species/genome corresponds to only one sequence. Example:

\>Genome1\
ATAGTAGATGAT..\
\>Genome2\
ATAGTAGTAGTAG..\
\>Genome3\
ATGATGATGATGATG..\
..\
etc.

options:

-h: print this help and exit\
-k <integer>: pattern weight (default 12)\
-t <integer>: numer of threads (default: 10)\
-s <integer>: the minimum score of a spaced-word match to be considered homologous (default: 0)


Scientific publications using filtered spaced word matches should cite:

C.-A. Leimeister, S. Sohrabi-Jahromi, B. Morgenstern (2017)
Fast and Accurate Phylogeny Reconstruction using Filtered Spaced-Word Matches
Bioinformatics 33, 971-979
