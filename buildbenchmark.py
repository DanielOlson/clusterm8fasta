#!/usr/bin/env python3

import os
import sys
import random
import torch
if len(sys.argv) != 5:
    print("Usage: buildbenchmark <clusters dir> <num queries> <num targets> <out_file>")
    exit()

cluster_dir = sys.argv[1]
num_queries = int(sys.argv[2])
num_targets = int(sys.argv[3])
out_Q = 'Q_' + sys.argv[4]
out_T = 'T_' + sys.argv[4]



class Cluster:
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = self.file_path[self.file_path.rfind("/") + 1:]
        self.name = self.filename[:file_path.rfind('_')]
        self.size = int(self.filename[self.filename.rfind('_') + 1:self.filename.rfind('.')])

class Sequence:
    def __init__(self, header, seq, cluster_name):
        self.header = header
        self.seq = seq

        self.meta = header[header.find(':: ') + 3:]
        self.meta = self.meta.split(' ')
        #  try:
        self.pct_id = float(self.meta[0])
        self.q_start = int(self.meta[1])
        self.q_end = int(self.meta[2])
        self.t_start = int(self.meta[3])
        self.t_end = int(self.meta[4])
        self.cluster_name = cluster_name


#    except:
#        print("----")
    #        print(header)
    #        print(self.meta)


def get_all_clusters_in_dir(dir, min_size):
    clusters = []
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if not os.path.isdir(file_path) and file_path.endswith('.fa'):
            c = Cluster(file_path)
            if c.size >= min_size:
                clusters.append(c)

    return clusters

def get_all_clusters(dir, min_size):
    clusters = []
    for file in os.listdir(dir):
        d = os.path.join(dir, file)
        if os.path.isdir(d):
            clusters.extend(get_all_clusters_in_dir(d, min_size))
    return clusters


def read_cluster(cluster_file, min_length, min_pct_id):
    sequences = []
    with open(cluster_file, 'r') as file:
        cluster_name = cluster_file[cluster_file.rfind('/') + 1:cluster_file.rfind('.')]
        header = ""
        seq = ""
        for line in file:
            line = line.rstrip()
            if len(line) == 0:
                continue
            if line[0] == '>':
                if min_length <= len(seq) <= max_seq_len:
                    newSequence = Sequence(header, seq, cluster_name)
                    if newSequence.pct_id >= min_pct_id and newSequence.t_end - newSequence.t_start > (min_length / 2.0):
                        sequences.append(newSequence)

                header = line
                seq = ""
            else:
                seq += line
    return sequences

def read_all_clusters(clusters, min_clust_size, min_length, min_pct_id):
    cluster_sequences = []
    num_sequences = 0
    for c in clusters:
        new_sequences = read_cluster(c.file_path, min_length, min_pct_id)
        if (len(new_sequences) < min_clust_size):
            continue
        cluster_sequences.extend(new_sequences)
        num_sequences += len(new_sequences)

    return cluster_sequences, num_sequences

print("Getting clusters...", end=' ', flush=True)
clusters = get_all_clusters(cluster_dir, 0)
print(str(len(clusters)) + " found")
print("Reading sequences...", end=' ',flush=True)
sequences, total_seqs = read_all_clusters(clusters, 0, 0, 0)

print("Writing sequences", end=" ", flush=True)

random.seed()

fileQ = open(out_Q, 'w')
fileT = open(out_T, 'w')

#num_queries = int(sys.argv[2])
#num_seqs = int(sys.argv[3])


used_seqs = dict()
used_seqs[-1] = True
for i in range(num_queries):
    #grab random sequence
    seq = -1
    while seq in used_seqs:
        seq = random.randrange(0, len(sequences))
    used_seqs[seq] = True

    seq = sequences[seq]
    fileQ.write(seq.header + "\n" + seq.seq + "\n")

for i in range(num_targets):
    # grab random sequence
    seq = -1
    while seq in used_seqs:
        seq = random.randrange(0, len(sequences))
    used_seqs[seq] = True

    seq = sequences[seq]
    fileT.write(seq.header + "\n" + seq.seq + "\n")

fileQ.close()
fileT.close()

print("Done.", flush=True)