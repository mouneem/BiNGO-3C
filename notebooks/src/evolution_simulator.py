import random
# generate a sequence of length n
def generate_random_seq(n = 10, alphabets='ACTG'):
    return ''.join(random.choices(alphabets,k=n))

# mutate seq
def mutate_seq(seq, alphabets='ACTG'):
    L = len(seq)
    i = random.randint(0, L-1) # position to mutate
    x = random.choices(alphabets,k=1)[0]
    while x == seq[i]: # check if different 
        x = random.choices(alphabets,k=1)[0] # apply mutation if not
    seq = seq[:i] + x + seq[i+1:] # insert new mutated base in sequence
    return seq

# add DEL to seq
def del_seq(seq):
    n = len(seq)
    i = random.randint(0, n)
    seq = seq[:i] + '' + seq[i+1:]
    return seq

# add INS to seq
def insert_seq(seq, alphabets='ACTG'):
    n = len(seq)
    i = random.randint(0, n)
    x = random.choices(alphabets,k=1)[0]
    seq = seq[:i+1] + x + seq[i+1:]
    return seq

# add %p mutation to seq
def add_p_mutations(seq, p = 0.1, alphabets='ACTG'): # p = 0.001 ~ 0.999
    n = int(len(seq) * p )
    for k in range(n):
        L = len(seq)
        i = random.randint(0, L-1) # position to mutate
        x = random.choices(alphabets,k=1)[0]
        if random.random() < 25 / 100.:
            seq = del_seq(seq)
        if random.random() < 25 / 100.:
            seq = insert_seq(seq,alphabets)
        else:
            while x == seq[i] : # check if different 
                x = random.choices(alphabets,k=1)[0] # apply mutation if not
            seq = seq[:i] + x + seq[i+1:] # insert new mutated base in sequence
    return seq

# add n mutation to seq
def add_n_mutations(seq, n,alphabets='ACTG',mutation_types='SIDT'):
    for i in range(n):
        type = random.choices(mutation_types,k=1)[0] # randomly select type: SUB INSERT or DELETE  
        if type == 'D':
            seq = insert_seq(seq,alphabets)
        elif type == 'I':
            seq = del_seq(seq)
        else:
            seq = mutate_seq(seq,alphabets)
    return seq

def to_fasta(sequence,id,path='../data/simulated_dataset1/'):
    file=open(path+str(id)+'.fasta','w+')
    file.write('>'+str(id)+'\n')
    file.write(sequence.replace('\n',''))

def dict_to_fasta(dict,path='../data/simulated_dataset2/'):
    file=open(path+'simulated_dataset.fasta','a+')
    for id in dict:
        sequence=dict[id]
        file.write('>'+str(id)+'\n')
        file.write(sequence.replace('\n','')+'\n')