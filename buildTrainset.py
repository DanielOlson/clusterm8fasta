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


def get_all_clusters_in_dir(dir, min_size):
    clusters = []
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if not os.path.isdir(file_path) and file_path.endswith('.fa'):
            c = Cluster(file_path)
            if c.size > min_size:
                clusters.append(c)

    return clusters

def get_all_clusters(dir, min_size):
    clusters = []
    for file in os.listdir(dir):
        d = os.path.join(dir, file)
        if os.path.isdir(d):
            clusters.extend(get_all_clusters_in_dir(d, min_size))
    return clusters

def

print("Getting clusters...", end=' ')
clusters = get_all_clusters(cluster_dir, min_clust_size)
print(str(len(clusters)) + " found")
print("Reading sequences...", end=' ')


