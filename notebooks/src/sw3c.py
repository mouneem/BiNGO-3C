### to do :replace kmers with subseq or words
### todo : rename functions
def dict_of_seqs_from_file(file = ''):
    """
    inputs:
        -path:  fasta   files
    outputs:
        return a dict of sequences 
        ex: 
            {
                id1 :   sequence1,
                id2 :   sequence2,
                ...
            }
    """
    sequences = {}
    content = open(file, 'r+').read().split('>')
    for seq in content:
        if seq != '':
            end_line = seq.find('\n') # end of 1st line
            id_pos = seq.find('.') # end of 1st line
            sequences[seq[:end_line]] = seq[end_line:].replace('\n', '') # select non id lines and remove backlines
    return sequences

def getKmersDict(dictSeq:dict, k, step):
    dictKmers = {} # {acc:kmers}
    for key, sequence in dictSeq.items():
        dictKmers[key] = set()
        start = 0
        end = k
        while end < len(sequence): #while the end of sequence is not reached
            dictKmers[key].add(sequence[start:end])
            start = start + step
            end = end + step
    return dictKmers


from os import listdir
from os.path import isfile, join

def getKmersSeq(sequence:str, k, step):
    kmers = [] 
    start = 0
    end = k
    #window = k - step
    while end < len(sequence):
        kmers.append(sequence[start:end])
        start = start + step
        end = end + step
    return kmers

def get_unique_Kmers(sequence, k, step):
    kmers = [] 
    start = 0
    end = k
    #window = k - step
    while end < len(sequence):
        kmers.append(sequence[start:end])
        start = start + step
        end = end + step
    return list(set(kmers))


def dict_kmer_of_seqs(dict_seqs, k = 11, step = 1):
    dict_kmers = {}
    for seq in dict_seqs:
        dict_kmers[seq] = get_unique_Kmers(dict_seqs[seq], k, step)
    return dict_kmers


import string
import random
import re

def random_delimiter(n = 11): # choose a random combination of ATGC of size n
    string = ''
    for i in range(n):
        b = random.sample("ATGC",1)
        string += b[0]
    return string

def random_delimiter_from_seq(seq , n = 7): # choose a random combination of ATGC of size n
    i = random.randint(1, len(seq)-1)
    return seq[i:i+n]

def get_pos_of_delimiter(sequence , delemiter): # find position of a delimiter (Can be Randomly selected)
    return [m.start() for m in re.finditer('(?='+delemiter+')', sequence)]


def dictSubSeq_from_dictSeq(dictSeq, delimiter): #split a sequence using positions (generate sub-sequences)
    dictSubSeq = {} # {accession : [subseq1, subseq2 ...] ..} 
    for key, sequence in dictSeq.items():
        posistions = get_pos_of_delimiter(sequence, delimiter )
        dictSubSeq[key] = set() # init position as set to avoid duplicated
        posistions = [0]+ posistions + [len(sequence)]
        for i in range(1,len(posistions)):
            dictSubSeq[key].add(sequence[ posistions[i-1] : posistions[i] ]) # add slice
    return(dictSubSeq)


def dictSubSeq_from_Fasta_file(filename): #read fasta file of subsequences and split a sequence using positions (generate sub-sequences)
    lines = open(filename,'r').readlines()
    SubSeqDict = {}
    for line in lines:
        line = line.replace('\n','')
        if '>' in line:
            id = '.'.join(line[1:].split('.')[:2])
            if id not in SubSeqDict.keys():
                SubSeqDict[id] = []
        else:
            SubSeqDict[id].append(line) # merge multiple lines into one
    return SubSeqDict




from os import listdir
from os.path import isfile, join

def dictSubSeq_from_repo(repo): #read all files in a repo and split them into subseqs
    SubSeqDict = {}
    c = 0
    files = [repo + '/' + f for f in listdir(repo) if isfile(join(repo, f))]
    for filename in files:
        c+=1
        lines = open(filename,'r').readlines()
        id = '.'.join(lines[0][1:].split('.')[:2]) #name of this file
        SubSeqDict[id] = ''
        Sequences = [] # new set of sequences
        Seq = ''
        for line in lines:
            line = line.replace('\n','')
            if '>' in line:
                Sequences.append(Seq)
                Seq = ''
            else:
                Seq += line # merge multiple lines into one
        SubSeqDict[id]=Sequences 
    return SubSeqDict
    

def list_of_subSequences_to_kmers(list_of_subSeqs, k = 11, step = 1):
    kmers= []
    for subSeq in list_of_subSeqs:
        kmers += getKmersSeq(subSeq, k, step)
    return(kmers)
    dictKmer = {}
    for key, subsequences in dictSubSeq.items():
        dictKmer[key] = set()
        kmers= []
        for subSeq in subsequences:
            kemerSeq = getKmersSeq(subSeq, k, step)
            if kemerSeq not in kmers:
                kmers += kemerSeq
        dictKmer[key] = set(kmers)
    return dictKmer


def compareSubsets(S1, S2):
    INT = S1.intersection(S2)
    UNI = S1.union(S2)
    return len(INT) / len(UNI)

def makePairs_KmerAccession(dictKmers):
    pairs = []
    for key, items in dictKmers.items():
        for item in items:
            pairs.append([key, item])
    return pairs



def dict_of_seqs_from_file(file = ''): #return a dict of seqs from fasta file {acc:seq,...}
    sequences = {}
    content = open(file, 'r+').read().split('>')
    for seq in content:
        if seq != '':
            end_line = seq.find('\n') # end of 1st line
            id_pos = seq.find('.') # end of 1st line
            sequences[seq[:end_line]] = seq[end_line:].replace('\n', '') # select non id lines and remove backlines
    return sequences

def getKmersDict(dictSeq:dict, k, step):
    dictKmers = {} # {acc:kmers}
    for key, sequence in dictSeq.items():
        dictKmers[key] = set()
        start = 0
        end = k
        while end < len(sequence): #while the end of sequence is not reached
            dictKmers[key].add(sequence[start:end])
            start = start + step
            end = end + step
    return dictKmers



def getKmersSeq(sequence:str, k, step):
    kmers = [] 
    start = 0
    end = k
    #window = k - step
    while end < len(sequence):
        kmers.append(sequence[start:end])
        start = start + step
        end = end + step
    return kmers

def get_unique_Kmers(sequence, k, step):
    kmers = [] 
    start = 0
    end = k
    #window = k - step
    while end < len(sequence):
        kmers.append(sequence[start:end])
        start = start + step
        end = end + step
    return list(set(kmers))


def dict_kmer_of_seqs(dict_seqs, k = 11, step = 1):
    dict_kmers = {}
    for seq in dict_seqs:
        dict_kmers[seq] = get_unique_Kmers(dict_seqs[seq], k, step)
    return dict_kmers


import string
import random
import re

def random_delimiter(n = 11): # choose a random combination of ATGC of size n
    string = ''
    for i in range(n):
        b = random.sample("ATGC",1)
        string += b[0]
    return string

def random_delimiter_from_seq(seq , n = 7): # choose a random combination of ATGC of size n
    i = random.randint(1, len(seq)-1)
    return seq[i:i+n]

def get_pos_of_delimiter(sequence , delemiter): # find position of a delimiter (Can be Randomly selected)
    return [m.start() for m in re.finditer('(?='+delemiter+')', sequence)]


def dictSubSeq_from_dictSeq(dictSeq, delimiter): #split a sequence using positions (generate sub-sequences)
    dictSubSeq = {} # {accession : [subseq1, subseq2 ...] ..} 
    for key, sequence in dictSeq.items():
        posistions = get_pos_of_delimiter(sequence, delimiter )
        dictSubSeq[key] = set() # init position as set to avoid duplicated
        posistions = [0]+ posistions + [len(sequence)]
        for i in range(1,len(posistions)):
            dictSubSeq[key].add(sequence[ posistions[i-1] : posistions[i] ]) # add slice
    return(dictSubSeq)


def list_of_subSequences_to_kmers(list_of_subSeqs, k = 11, step = 1):
    kmers= []
    for subSeq in list_of_subSeqs:
        kmers += getKmersSeq(subSeq, k, step)
    return(kmers)

def dictKmer_from_DictSubseq(dictSubSeq, k = 11, step = 1): 
    dictKmer = {}
    for key, subsequences in dictSubSeq.items():
        dictKmer[key] = set()
        kmers= []
        for subSeq in subsequences[2:]:
            kemerSeq = getKmersSeq(subSeq, k, step)
            if kemerSeq not in kmers:
                kmers += kemerSeq
        bin = binarize_a_list(kmers)
        dictKmer[key]|= set(bin) # change to binary representation
    return dictKmer


def compareSubsets(S1, S2):
    INT = S1.intersection(S2)
    UNI = S1.union(S2)
    return len(INT) / len(UNI)

def makePairs_KmerAccession(dictKmers):
    pairs = []
    for key, items in dictKmers.items():
        for item in items:
            pairs.append([key, item])
    return pairs


### Compression:
# input: sub-sequence: AT
# output: binary version: 0011
def binarization(seq):
    map = {'A':'00','C':'01','G':'10','T':'11'}
    binare = seq
    for ch, bi in map.items():
        binare = binare.upper().replace(ch, bi)
    binare = ''.join([c for c in binare if c in '01']) # remove any other char
    if len(binare)<1:
        return 'A'
    return int(binare, base=2)

# input: list of sub-sequences
# output: list of binary values
def binarize_a_list(lst):
    return [ binarization(e) for e in lst]