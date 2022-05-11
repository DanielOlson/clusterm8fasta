#!/usr/bin/env python3

import os
import sys

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
        self.filename = self.file_path[self.file_path.rfind("/") + 1:]
        self.name = self.filename[:file_path.rfind('_')]
        self.size = int(self.filename[file_path.rfind('_') + 1:file_path.rfind('.')])

class Sequence:
    def __init__(self, header, seq):
        self.header = header
        self.seq = seq
        self.meta = header[header.find('::') + 3:]
        self.meta = self.meta.split(' ')

        self.pct_id = float(self.meta[0])
        self.q_start = int(self.meta[1])
        self.q_end = int(self.meta[2])
        self.t_start = int(self.meta[3])
        self.t_end = int(self.meta[4])


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
        cluster_sequences.append(new_sequences)
        num_sequences += len(new_sequences)

    return cluster_sequences, num_sequences


print("Getting clusters...", end=' ')
clusters = get_all_clusters(cluster_dir, min_clust_size)
print(str(len(clusters)) + " found")
print("Reading sequences...", end=' ')
clusters, num_seqs = read_all_clusters(clusters, min_clust_size, min_seq_len, min_pct_id)
print(str(clusters) + " clusters remain. " + str(num_seqs) + " sequences")

