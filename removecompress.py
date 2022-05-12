import os
import sys

if len(sys.argv) != 3:
    print("Usage: removecompress <trainingdir> <compress_dir>")

train_dir = sys.argv[1]
compress_dir = sys.argv[2]

compression_targets = []
removal_targets = []

for subdir in os.listdir(train_dir):
    zip_name = subdir
    if zip_name.endswith('/'):
        zip_name = zip_name[:-1]
    zip_name += ".zip"
    subdir = os.path.join(train_dir, subdir)

    zip_name = os.path.join(compress_dir, zip_name)
    if os.path.isdir(subdir):
        compression_targets.append((subdir, zip_name))

        for file in os.listdir(subdir):
            file = os.path.join(subdir, file)
            if not os.path.isdir(file):
                if file.endswith('.post')
                    removal_targets.append(file)

for i in removal_targets:
    print("rm -f " + i)

for dir, name in compression_targets:
    print("zip -r " + name + " " + dir)

