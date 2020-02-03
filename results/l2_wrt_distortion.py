#!/usr/bin/env python
import sys
from numpy import median

# result after running in bash shell:
# ls experiment_E/parameter_2000_2000/snapshot_000*/start_0010/stderr.out experiment_E/parameter_2000_2000/snapshot_000*/start_0020/stderr.out

# files = ['experiment_C/parameter_0000_0000/snapshot_0001/start_0010/stderr.out']
files = ['experiment_D/parameter_2000_0000/snapshot_0001/start_0010/stderr.out']

# files = sys.argv[1:]
files.sort()
broken = set()
ID = None
broken_record = []
TOTAL = 1000
for each_file in files:
    with open(each_file) as f:
        for line in f:
            if line[:10] == 'evaluating':
                tags = line.split()
                ID = int(tags[1])
            elif line[:12] == 'attack: step':
                tags = line.split()[-7:]
                l2_loss =  float(tags[0])
                true_label = int(tags[-3].split(',')[0])
                predict_label = int(tags[-1].split('[')[-1].split(']')[0])
                if true_label != predict_label and ID not in broken:
                    broken.add(ID)
                    broken_record.append((l2_loss, ID))
            elif line[:6] == "true =":
                 tags = line.split()
                 true_label = int(tags[2][:-1])
                 predict_label = int(tags[-1])
                 if ID in broken and true_label == predict_label:
                     broken.remove(ID)
                     broken_record.pop()

broken_record.sort()
# debug
# print(broken_record)
acc = []
for i in range(len(broken_record)):
    TOTAL -= 1
    if i == 0 or broken_record[i][0] != broken_record[i-1][0]:
        acc.append((broken_record[i][0], TOTAL))
for each in acc:
    print("%f,%d"%(each[0],each[1]))

