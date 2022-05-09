import os
import sys


if len(sys.argv) != 5:
    print("Usage: UnirefClusterer <m8_filepath> <target_fasta> <out_dir> <files_per_dir>")
    print("Example: UnirefClusterer ./unireffile.m8 uniref90.fasta ./clusters/ 160")
    exit(0)

m8_filepath = sys.argv[1]
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
                queries[query].targets[target] = (pct_id, q_start, q_end, t_start, t_end, "")

            else:
                queries[query] = QueryEntry()
                queries[query].targets[target] = (pct_id, q_start, q_end, t_start, t_end, "")

            if target in targets:
                targets[target].append(query)
            else:
                targets[target] = [query]
    return queries, targets


def map_query_files(queries, base_dir, files_per_dir):
    i = 0
    cdir = ""
    for query in queries:
        if i % files_per_dir == 0:
            cdir = os.path.join(base_dir, "cg_" + str(int(i / files_per_dir)) + "/")

        queries[query].dir = cdir
        queries[query].file = os.path.join(cdir, query + "_" + str(len(query.targets)) + ".fa")

        i += 1


def fill_queries(queries, targets, fasta_file):



queries, targets = map_query_targets(m8_filepath)
map_query_files(queries, out_dir, files_per_dir)
fill_queries(queries, targets, target_fasta)


