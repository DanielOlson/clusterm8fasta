import sys
import numpy as np
import re

def ReadPosteriors(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        found_dump = False
        read_line_count = 0
        for line in file:
            if not found_dump:
                if "POSTERIOR DUMP" in line:
                    found_dump = True
                    continue

            else:
                row = []
                if "END DUMP" in line:
                    break
                if read_line_count >= 2:
                    line = line.strip()
                    line = re.split(" +", line)
                    if len(line) == 1:
                        continue

                    if line[1] != 'M':
                        continue
                    for i in range(2, len(line)):
                        if line[i] == '-inf':
                            val = -1000000
                        else:
                            val = float(line[i])

                        row.append(val)

                    matrix.append(row)
                read_line_count += 1

    return np.array(matrix)


if len(sys.argv) < 3:
    print("Usage: posttonp <out_file> <in_files>")

out_file = sys.argv[1]
in_files = sys.argv[2:]


npmats = {f:ReadPosteriors(f) for f in in_files}
np.savez(out_file, **npmats)