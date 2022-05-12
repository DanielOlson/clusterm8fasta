import sys
from math import ceil
import os

if len(sys.argv) != 5:
    print("Usage: splittrainingfile <in_file_1> <in_file_2> <dir> <sequences_per_subdir>")
    exit(0)

in_file1 = sys.argv[1]
in_file2 = sys.argv[2]
dir = sys.argv[3]
seqs_per_dir = int(sys.argv[4])

in_file1 = open(in_file1)
in_file2 = open(in_file2)


lines1 = in_file1.readlines()
lines2 = in_file2.readlines()

if len(lines1) != len(lines2):
    print("unequal number of lines!")
    exit(-1)

total_bytes = 0

header1 = ""
seq1 = ""

header2 = ""
seq2 = ""

sequences_1 = []
sequences_2 = []

print("Reading sequences from training set")
for i in range(len(lines1)):
    if i % 2 == 0:
        if len(header1) > 0:
            sequences_1.append((header1, seq1))
        if len(header2) > 0:
            sequences_2.append((header2, seq2))

        header1 = lines1[i]
        header2 = lines2[i]
    else:
        seq1 = lines1[i]
        seq2 = lines2[i]

in_file1.close()
in_file2.close()
if len(sequences_1) != len(sequences_2):
    print("number of sequences are not equal to eachother")
    exit(-1)

print("Found " + str(len(sequences_1)) + " sequences")

# Create directories and output files.
num_dirs = ceil((2 * len(sequences_1)) / seqs_per_dir)
print("Creating", num_dirs, "directories")
for i in range(num_dirs):
    path = os.path.join(dir, "sub_" + str(i))
    if not os.path.isdir(path):
        os.mkdir(path)

print("Writing sequence pairs")
for i in range(len(sequences_1)):
    subdir = os.path.join(dir, "sub_" + str(i % num_dirs) + "/")
    fileA = os.path.join(subdir, "A_" + str(i) + ".fa")
    fileB = os.path.join(subdir, "B_" + str(i) + ".fa")

    fileA = open(fileA, 'w')
    fileB = open(fileB, 'w')

    fileA.write(sequences_1[i][0] + "\n")
    fileA.write(sequences_1[i][1] + "\n")

    fileB.write(sequences_2[i][0] + "\n")
    fileB.write(sequences_2[i][1] + "\n")

    fileA.close()
    fileB.close()

print("Done.")