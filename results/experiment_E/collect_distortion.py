import sys
# import ipdb
fNameList = sys.argv[1:]

# debug
# p3 collect_distortion.py $(ls snapshot_0003/star*/stderr.out)
#
# fNameList = ['snapshot_0001/start_0000/stderr.out', 'snapshot_0002/start_0000/stderr.out',
#        'snapshot_0003/start_0000/stderr.out']

correct = False
current_id = None
fail_distortion = dict()
normal_distortion = dict()
last_distortion = dict()

for fName in fNameList:
    with open(fName) as f:
        for line in f:
            if line[:10] == 'evaluating':
                current_id = int(line.split()[1])

            elif line[:7] == 'attack:':
                splited = line.split()
                l2_loss = float(splited[10])
                true_label = splited[14][:-1]
                predict_label = splited[16][1:-2]
                correct = true_label == predict_label
                # ipdb.set_trace()

                if correct:
                    if current_id not in normal_distortion:
                        normal_distortion[current_id] = l2_loss
                    else:
                        normal_distortion[current_id] = max(l2_loss, normal_distortion[current_id])
                else:
                    if current_id not in fail_distortion:
                        fail_distortion[current_id] = l2_loss
                    else:
                        fail_distortion[current_id] = min(l2_loss, fail_distortion[current_id])

# print(normal_distortion)
# print(fail_distortion)

for k in normal_distortion:
    if k in fail_distortion:
        last_distortion[k] = normal_distortion[k]

for k in last_distortion:
    print("%d,%f" % (k,last_distortion[k]))



