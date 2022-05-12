import os
import sys

if len(sys.argv) != 3:
    print("Usage: buildpdbash <training sequence dir> <post dump path>")

dir = sys.argv[1]
post_dump_path = sys.argv[2]

def create_script_for_dir(subdir):

    A_seqs = dict()
    B_seqs = dict()
    # get all sequences
    for fasta_file in os.listdir(subdir):

        file_path = os.path.join(subdir, fasta_file)


        if os.path.isfile(file_path) and file_path.endswith('.fa'):
            if fasta_file.startswith("A_"):
                A_seqs[fasta_file] = file_path

            if fasta_file.startswith("B_"):
                B_seqs[fasta_file] = file_path

    #verify A seqs and B seqs
    if len(A_seqs) != len(B_seqs):
        print("unequal number of A and B sequences.")
        exit(-1)


    for file_A in A_seqs:
        B_version = 'B' + file_A[1:]
        if not B_version in B_seqs:
            print(file_A, "has no counterpart", B_version)
            exit(-1)


    file_path = os.path.join(subdir, "postdump.sh")
    with open(file_path, 'w') as f:
        f.write("module load python3\n")

        for file_A in A_seqs:
            file_B = 'B' + file_A[1:]

            out = file_A[2:-3]
            out = out + ".post"

            file_A = os.path.join(subdir, file_A)
            file_B = os.path.join(subdir, file_B)
            out = os.path.join(subdir, out)

            f.write(post_dump_path + " " + file_A + " " + file_B + " > " + out + "\n")


        f.write("python3 ~/scripts/clusterm8fasta/posttonp.py " + subdir + "/" "post.npz " + subdir + "/*.post\n")
        f.write("rm *.post\n")





print("Creating bash scripts...")
for file in os.listdir(dir):
    file = os.path.join(dir, file)
    if os.path.isdir(file):
        create_script_for_dir(file)

print("Done.")