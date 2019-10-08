#!/usr/bin/env python
import sys
from numpy import median
# debug
# print(sys.argv[1:])

def scan_file(filename, threshold=14.95):
    # directly recording the list of values
    res = []
    count = 0
    total = 0
    smaller_count = 0
    with open(filename) as f:
        for line in f:
            if len(line)>19 and line[:19]=='attack: step 30/30,':
                loss=float(line.split()[10])
                count += 1
                total += loss
                # add
                res.append(loss)
                if loss < threshold:
                    smaller_count += 1
    return count, total, smaller_count, res 

count = 0
total = 0
smaller_count = 0
res = []
for each_file in sys.argv[1:]:
    d_count, d_total, d_smaller_count, tmp_res = scan_file(each_file)
    count += d_count
    total += d_total
    smaller_count += d_smaller_count
    res += tmp_res

print ("number: ", count, "average: ", total/count, "median: ", median(res), "smaller count: ", smaller_count)

