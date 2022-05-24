import os
import sys
import re

if len(sys.argv) != 2:
    print("Usage: parsehprefilter.py <input file>")
    exit(0)

input_file = sys.argv[1]

passed_MSV = 0
passed_bias = 0
passed_viterbi = 0
passed_forward = 0

with open(input_file, 'r') as file:
    lines = file.readlines()
    stage = 0
    for line in lines:

        if line.startswith("Passed MSV filter:"):
            m = re.search(r"\d", line)
            if m:
                start = m.start()
                passed = int(line[start:line.find(" ", start)])
                print(line, passed)



