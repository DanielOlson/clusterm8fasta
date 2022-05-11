#!/usr/bin/env python3

import os
import sys
import random
if len(sys.argv) != 7:
    print("Usage: buildTrainset <cluster_dir>  <min_seq_length> <min_pct_id> <min_cluster_size> <#sequence_pairs> <out_file>")
    print("Example: buildTrainset ./clusters/ 256  0.6 100 200000./clusters/ trainout.fa")
    print("Outputs two fasta files. E.g: A_trainout.fa and B_trainout.fa")
    exit(0)

cluster_dir = sys.argv[1]
min_seq_len = int(sys.argv[2])
min_pct_id = float(sys.argv[3])
min_clust_size = int(sys.argv[4])
num_seq_pairs = int(sys.argv[5])
out_1 = 'A_' + sys.argv[6]
out_2 = 'B_' + sys.argv[6]


class Cluster:
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = self.file_path[self.file_path.rfind("/") + 1:]
        self.name = self.filename[:file_path.rfind('_')]
        self.size = int(self.filename[self.filename.rfind('_') + 1:self.filename.rfind('.')])

class Sequence:
    def __init__(self, header, seq):
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

print("Getting clusters...", end=' ', flush=True)
clusters = get_all_clusters(cluster_dir, min_clust_size)
print(str(len(clusters)) + " found")
print("Reading sequences...", end=' ',flush=True)
clusters, total_seqs = read_all_clusters(clusters, min_clust_size, min_seq_len, min_pct_id)
print(str(len(clusters)) + " clusters remain. " + str(total_seqs) + " sequences", flush=True)

print("Writing random sequence pairs", end=" ", flush=True)

random.seed()

file1 = open(out_1, 'w')
file2 = open(out_2, 'w')

for i in range(num_seq_pairs):
    #grab a random cluster
    c = clusters[random.randint(0, len(clusters))]
    seq1 = 0
    seq2 = 0
    while seq1 == seq2:
        seq1 = random.randint(0, len(c))
        seq2 = random.randint(0, len(c))

    seq1 = c[seq1]
    seq2 = c[seq2]

    file1.write(seq1.header + " " + str(i) + "\n")
    file2.write(seq2.header + " " + str(i) + "\n")

    file1.write(seq1.seq + "\n")
    file2.write(seq2.seq + "\n")

file1.close()
file2.close()

print("Done.\n", flush=True)