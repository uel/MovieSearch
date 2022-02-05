import numpy as np
import scipy.sparse as sparse
import math
import os

def create_matrix():
    rows = {j : i for i, j in enumerate(open('data/terms.txt', 'r').read().splitlines())}
    columns = {j+".txt" : i for i, j in enumerate(open('data/documents.txt', 'r').read().splitlines())}
    document_freq = {j.split("\t")[0] : int(j.split("\t")[1]) for j in open('data/document_freq.txt', 'r').read().splitlines()}
    max_freq = {j.split("\t")[0] : int(j.split("\t")[1]) for j in open('data/max_freq.txt', 'r').read().splitlines()}

    r = []
    c = []
    v = []

    for i in os.listdir('data/tokenized'):
        with open('data/tokenized/' + i, 'r') as f:
            for line in f:
                term, freq = line.split("\t")
                if rows[term] >= 1:
                    continue
                weight = (int(freq)/max_freq[term])*math.log2(len(columns)/document_freq[term])
                r.append(rows[term])
                c.append(columns[i])
                v.append(weight)

    A = sparse.csr_matrix((v, (r, c)), shape=(1, len(columns)), dtype=np.float32)
    
    sparse.save_npz("data/matrix.npz", A)

create_matrix()