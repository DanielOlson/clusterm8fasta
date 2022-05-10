#!/usr/bin/env python3

import os
import sys
import

if len(sys.argv) != 7:
    print("Usage: buildTrainset <cluster_dir>  <min_seq_length> <min_pct_id> <min_cluster_size> <#sequence_pairs> <out_file>")
    print("Example: buildTrainset ./clusters/ 256  0.6 100 200000./clusters/ trainout.fa")
    print("Outputs two fasta files. E.g: A_trainout.fa and B_trainout.fa")
    exit(0)

cluster_dir = sys.argv[1]
min_seq_len = int(sys.argv[2])
pct_id = float(sys.argv[3])
min_clust_size = int(sys.argv[4])
num_seqs = int(sys.argv[5])
out_1 = 'A_' + sys.argv[6]
out_2 = 'B_' + sys.argv[6]


class Cluster:
    def __init__(self, file_path):
        self.file_path = file_path
        self.name = self.filename[:filename.rfind('_')]
        self.size = self.filename[filename.rfind('_') + 1:filename.rfind('.')]

class Sequence:
    def __init__(self, header, seq):
        self.header = header
        self.seq = seq
        self.pct_id = header[header.find('::') + 3:]
        self.pct_id = float(self.pct_id[:self.pct_id.find(' ')])

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
        header = ""
        seq = ""
        for line in file:
            line = line.rstrip()
            if len(line) == 0:
                continue
            if line[0] == '>':
                if len(seq) >= min_length:
                    newSequence = Sequence(header, seq)
                    if newSequence.pct_id >= min_pct_id:
                        sequences.append(newSequence)
                header = line
                seq = ""
            else:
                seq += line
    return sequences

def read_all_clusters(clusters, min_length, min_pct_id):
    cluster_sequences = []
    for c in clusters:
        #stopped right here


print("Getting clusters...", end=' ')
clusters = get_all_clusters(cluster_dir, min_clust_size)
print(str(len(clusters)) + " found")
print("Reading sequences...", end=' ')


