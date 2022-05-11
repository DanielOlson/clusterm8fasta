import os
import sys

if len(sys.argv) != 3:
    print("usage: getpostsize file1 file2")
    exit(0)

file1 = sys.argv[1]
file2 = sys.argv[2]

file1 = open(file1)
file2 = open(file2)


lines1 = file1.readlines()
lines2 = file2.readlines()

if len(lines1) != len(lines2):
    print("unequal number of lines!")
    exit(-1)

total_bytes = 0
for i in range(len(lines1)):
    if i % 2 == 0:
        continue
    total_bytes += len(lines1[i]) * (len(lines2[i]) + 5)

print(total_bytes)

file1.close()
file2.close()

