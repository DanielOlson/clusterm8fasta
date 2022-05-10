#!/usr/bin/env python3

import os
import sys


if len(sys.argv) != 5:
    print("Usage: clustersearch <m8_filepath>  <target_fasta> <out_dir> <files_per_dir>")
    print("Example: clustersearch ./unireffile.m8 uniref90.fasta ./clusters/ 160")
    exit(0)

m8_filepath = sys.argv[1]
query_fasta = sys.argv[2]
target_fasta = sys.argv[2]
out_dir = sys.argv[3]
files_per_dir = int(sys.argv[4])


class QueryEntry:
    def __init__(self):
        self.query = ""
        self.targets = dict()
        self.dir = ""
        self.file = ""


def map_query_targets(m8_file):

    queries = dict()
    targets = dict()

    with open(m8_file, "r") as file:
        for line in file:
            line = line.strip()
            line = line.split("\t")

            query = line[0]
            target = line[1]
            pct_id = line[2]
            q_start = line[6]
            q_end = line[7]
            t_start = line[8]
            t_end = line[9]

            if query in queries:
                queries[query].targets[target] = (pct_id, q_start, q_end, t_start, t_end)


            else:
                queries[query] = QueryEntry()
                queries[query].query = query
                queries[query].targets[target] = (pct_id, q_start, q_end, t_start, t_end)

            if target not in targets:
                targets[target] = ("", "")

    return queries, targets


def map_query_files(queries, base_dir, files_per_dir):
    i = 0
    cdir = ""
    dir_num = 0
    for query in queries:
        if i % files_per_dir == 0:
            cdir = os.path.join(base_dir, "cg_" + str(dir_num) + "/")
            dir_num += 1

        queries[query].dir = cdir
        queries[query].file = os.path.join(cdir, query + "_" + str(len(queries[query].targets)) + ".fa")

        i += 1


def fill_targets(targets, fasta_file):
    seq_header = ""
    seq = ""

    with open(fasta_file, "r") as file:
        for line in file:
            line.strip()
            if line[0] == '>':
                if len(seq_header) > 0 and len(seq) > 0:
                    target = seq_header[1:seq_header.find(' ')]
                    if target in targets:
                        targets[target] = (seq_header, seq)
                seq_header = line
                seq = ""
            else:
                seq += line

        if len(seq_header) > 0 and len(seq) > 0:
            target = seq_header[1:seq_header.find(' ')]
            if target in targets:
                targets[target] = (seq_header, seq)



def write_query(query, targets):
    with open(query.file, 'w') as file:
        for t in query.targets:
            print(t, targets[t])
            header = targets[t][0]
            header += " :: " + query.targets[t][0]
            header += " " + query.targets[t][1]
            header += " " + query.targets[t][2]
            header += " " + query.targets[t][3]
            header += " " + query.targets[t][4]
            file.write(header)
            file.write(targets[t][1] + "\n")


def write_queries(queries, targets):
    for q in queries:
        if not os.path.isdir(queries[q].dir):
            os.mkdir(queries[q].dir)
        write_query(queries[q], targets)


print("Reading m8 file and mapping queries")
queries, targets = map_query_targets(m8_filepath)
print("Queries: " + str(len(queries)) + " Targets: " + str(len(targets)))
print("Mapping queries to files")
map_query_files(queries, out_dir, files_per_dir)
print("Reading targets")
fill_targets(targets, target_fasta)
print("Writing queries")
write_queries(queries, targets)
print("Done.")

