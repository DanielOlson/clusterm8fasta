import sys

if len(sys.argv) != 5:
    print("Usage: splittrainingfile <in_file_1> <in_file_2> <dir> <sequences_per_subdir>")
    exit(0)

in_file1 = sys.argv[1]
in_file2 = sys.argv[2]
dir = sys.argv[3]
seqs_per_dir = sys.argv[5]

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

file1.close()
file2.close()

if len(sequences_1) != len(sequences_2):
    print("number of sequences are not equal to eachother")
    exit(-1)

print("Found " + str(len(sequences_1)) + " sequences")

# Create directories and output files.

