import numpy as np
import sys
import pickle
import os

def evaluate(model, attack, provider, start=None, end=None, deterministic=False, debug=False, snapshot_adv=False):
    '''
    Evaluate an attack on a particular model and return attack success rate._adv

    An attack is allowed to be adaptive, so it's fine to design the attack
    based on the specific model it's supposed to break.

    `start` (inclusive) and `end` (exclusive) are indices to evaluate on. If
    unspecified, evaluates on the entire dataset.

    `deterministic` specifies whether to seed the RNG with a constant value for
    a more deterministic test (so randomly selected target classes are chosen
    in a pseudorandom way).
    '''

    if not provider.provides(model.dataset):
        raise ValueError('provider does not provide correct dataset')
    if start is not None and not (0 <= start < len(provider)):
        raise ValueError('start value out of range')
    if end is not None and not (0 <= end <= len(provider)):
        raise ValueError('end value out of range')

    threat_model = model.threat_model
    targeted = threat_model.targeted

    success = 0
    total = 0
    for i in range(start, end):
        print('evaluating %d of [%d, %d)' % (i, start, end), file=sys.stderr)
        total += 1
        x_snap, x_orig, y, snapshot_filename = provider[i] 
        target = None
        if targeted: 
            target = choose_target(i, y, model.dataset.labels, deterministic)
        # x_adv = attack.run(np.copy(x), y, target)
        x_adv = attack.run(np.copy(x_snap), np.copy(x_orig), y, target) 
        if not threat_model.check(np.copy(x_orig), np.copy(x_adv)):
            if debug:
                print('check failed', file=sys.stderr)
            # continue # do not skip the calculation
        y_adv = model.classify(np.copy(x_adv))
        if debug:
            print('true = %d, adv = %d' % (y, y_adv), file=sys.stderr)
        if targeted:
            if y_adv == target:
                success += 1
        else: # false by default
            if y_adv != y:
                success += 1

        # save adv to pkl file, can be run
        if snapshot_filename != None and snapshot_adv:
            os.makedirs(os.path.dirname(snapshot_filename), exist_ok=True)
            pickle.dump(x_adv, open(snapshot_filename, 'wb'))

    success_rate = success / total
    return success_rate

def choose_target(index, true_label, num_labels, deterministic=False):
    if deterministic:
        rng = np.random.RandomState(index)
    else:
        rng = np.random.RandomState()

    target = true_label
    while target == true_label:
        target = rng.randint(0, num_labels)

    return target
