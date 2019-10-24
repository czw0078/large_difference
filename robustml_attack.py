# silence
# import robustml
import robustml_dev as robustml
from robustml_model import InputTransformations
import sys
import argparse
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import numpy as np
import os
os.environ['KMP_AFFINITY']='compact'

class NA(robustml.attack.Attack): # no attack at all
    def __init__(self, sess, model, epsilon, max_steps=1, learning_rate=0.1, lam=1e-6, debug=False):
        self._sess = sess

        self._model = model
        self._input = model.input
        self._l2_input = tf.placeholder(tf.float32, self._input.shape) 
        self._original = tf.placeholder(tf.float32, self._input.shape)
        self._label = tf.placeholder(tf.int32, ())
        one_hot = tf.expand_dims(tf.one_hot(self._label, 1000), axis=0)
        # adaptable to batch input, if only one image, the output shape is just (1, 1000)
        ensemble_labels = tf.tile(one_hot, (model.logits.shape[0], 1))
        self._l2 = tf.sqrt(2*tf.nn.l2_loss(self._l2_input - self._original)) # l2_input is the adv
        self._xent = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=model.logits, labels=ensemble_labels))
        self._loss = lam * tf.maximum(self._l2 - epsilon, 0) + self._xent # regularize when self._l2 larger than epsilon 
        self._grad, = tf.gradients(self._loss, self._input)

        self._epsilon = epsilon
        self._max_steps = max_steps
        self._learning_rate = learning_rate
        self._debug = debug

    def run(self, x_adv, x_orig, y, target):
        if target is not None:
            raise NotImplementedError
        p, ll2, lxent, g = self._sess.run(
	    [self._model.predictions, self._l2, self._xent, self._grad],
	    {self._input: x_orig, self._label: y, self._l2_input: x_orig, self._original: x_orig}
        )
        if self._debug:
            print(
                'attack: step %d/%d, xent loss = %g, l2 loss = %g (max %g), (true %d, predicted %s)' % (
                1,
                self._max_steps,
                lxent,
                ll2,
                self._epsilon,
                y,
                p), file=sys.stderr)
        return x_orig

class PGD(robustml.attack.Attack): # max_steps = 1000
    def __init__(self, sess, model, epsilon, max_steps=20, learning_rate=0.1, lam=1e-6, debug=False, early_stop=True):
        self._sess = sess
        # debug
        print(early_stop)
        self._model = model
        self._input = model.input
        self._l2_input = tf.placeholder(tf.float32, self._input.shape) 
        self._original = tf.placeholder(tf.float32, self._input.shape)
        self._label = tf.placeholder(tf.int32, ())
        one_hot = tf.expand_dims(tf.one_hot(self._label, 1000), axis=0)
        # adaptable to batch input, but the output shape always (1, 1000)
        ensemble_labels = tf.tile(one_hot, (model.logits.shape[0], 1))
        self._l2 = tf.sqrt(2*tf.nn.l2_loss(self._l2_input - self._original)) # l2_input is the adv
        self._xent = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=model.logits, labels=ensemble_labels))
        self._loss = lam * tf.maximum(self._l2 - epsilon, 0) + self._xent # regularize when self._l2 larger than epsilon 
        self._grad, = tf.gradients(self._loss, self._input)

        self._epsilon = epsilon
        self._max_steps = max_steps
        self._learning_rate = learning_rate
        self._debug = debug
        self._early_stop = early_stop

    def run(self, x_adv, x_orig, y, target): 
        if target is not None:
            raise NotImplementedError
        # adv = np.copy(x) 
        for i in range(self._max_steps):
            p, ll2, lxent, g = self._sess.run(
                [self._model.predictions, self._l2, self._xent, self._grad],
                {self._input: x_adv, self._label: y, self._l2_input: x_adv, self._original: x_orig}
            )
            if self._debug:
                print(
                    'attack: step %d/%d, xent loss = %g, l2 loss = %g (max %g), (true %d, predicted %s)' % (
                        i+1,
                        self._max_steps,
                        lxent,
                        ll2,
                        self._epsilon,
                        y,
                        p
                    ),
                    file=sys.stderr
                )
            if self._early_stop and y not in p and ll2 < self._epsilon:
                # we're done
                if self._debug:
                    print('returning early', file=sys.stderr)
                break
            x_adv += self._learning_rate * g
            x_adv = np.clip(x_adv, 0, 1)
        return x_adv

class BPDA(robustml.attack.Attack):
    def __init__(self, sess, model, epsilon, 
            max_steps=1000, learning_rate=0.1, lam=1e-6, debug=False, 
            n_shapes=200, type_primitive='1', tmp_index=1, tmp_dir='./ram',
            early_stop=True, unbound=True): 
        self._sess = sess
        self._n_shapes=n_shapes
        self._model = model
        self._input = model.input
        self._l2_input = tf.placeholder(tf.float32, self._input.shape) # using BPDA, so we want this to pass the original adversarial example
        self._original = tf.placeholder(tf.float32, self._input.shape)
        self._label = tf.placeholder(tf.int32, ())
        one_hot = tf.expand_dims(tf.one_hot(self._label, 1000), axis=0)
        ensemble_labels = tf.tile(one_hot, (model.logits.shape[0], 1))
        self._l2 = tf.sqrt(2*tf.nn.l2_loss(self._l2_input - self._original))
        self._xent = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=model.logits, labels=ensemble_labels))
        self._loss = lam * tf.maximum(self._l2 - epsilon, 0) + self._xent
        self._grad, = tf.gradients(self._loss, self._input)

        self._epsilon = epsilon
        self._max_steps = max_steps
        self._learning_rate = learning_rate
        self._debug = debug
        self._early_stop = early_stop
        self._unbound = unbound
        self._type_primitive = type_primitive
        self._tmp_index = tmp_index
        self._tmp_dir = tmp_dir

    def run(self, x_adv, x_orig, y, target):
        if target is not None:
            raise NotImplementedError
        # adv = np.copy(x)
        for i in range(self._max_steps):
            adv_def = self._model.defend(x_adv, self._n_shapes, self._type_primitive, self._tmp_index, self._tmp_dir) # n_shapes_attack
            p, ll2, lxent, g = self._sess.run(
                [self._model.predictions, self._l2, self._xent, self._grad],
                {self._input: adv_def, self._label: y, self._l2_input: x_adv, self._original: x_orig}
            )
            if self._debug:
                print(
                    'attack: step %d/%d, xent loss = %g, l2 loss = %g (max %g), (true %d, predicted %s)' % (
                        i+1,
                        self._max_steps,
                        lxent,
                        ll2,
                        self._epsilon,
                        y,
                        p # the p is not the final prediction, because adv need to be (0,1)
                    ),
                    file=sys.stderr
                )
            if self._early_stop and y not in p and ll2 < self._epsilon:
                # we're done
                if self._debug:
                    print('returning early', file=sys.stderr)
                break
            if self._early_stop and y not in p and self._unbound:
                # we're done
                if self._debug:
                    print('unbound attack returning early', file=sys.stderr)
                break
            x_adv += self._learning_rate * g
            x_adv = np.clip(x_adv, 0, 1)
        return x_adv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imagenet-path', type=str, required=True,
            help='directory containing `val.txt` and `val/` folder')
    parser.add_argument('--defense', type=str, required=True,
            help='none | bitdepth | primitive ')
    parser.add_argument('--attack', type=str, required=True,
            help='none | PGD | BPDA ')
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--end', type=int, default=1) # change for at least 10
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--snapshot_adv', action='store_true')
    parser.add_argument('--n_snapshot', type=int, default=-1) 
    parser.add_argument('--early_stop', action='store_true')
    parser.add_argument('--unbound', action='store_true')
    parser.add_argument('--n_shapes_defense', type=int, default=200)
    parser.add_argument('--n_shapes_attack_BPDA', type=int, default=200)
    parser.add_argument('--max_steps_attack', type=int, default=20)
    parser.add_argument('--type_primitive_attack_BPDA', type=str, default='1')
    parser.add_argument('--type_primitive_defense', type=str, default='1')
    parser.add_argument('--primitive_tmp_dir', type=str, default='./ram')
    args = parser.parse_args()
    
    # use the parameter as the tag and start
    tag="{0:04d}_{1:04d}".format(args.n_shapes_defense, args.n_shapes_attack_BPDA)

    # set up TensorFlow session
    sess = tf.Session()

    # initialize a model
    model = InputTransformations(sess, args.defense, 
        args.n_shapes_defense, args.type_primitive_defense, args.start, args.primitive_tmp_dir) # n_shapes_defense

    # initialize an attack (it's a white box attack, and it's allowed to look
    # at the internals of the model in any way it wants)

    if args.attack=='BPDA':
        attack = BPDA(sess, model, model.threat_model.epsilon, debug=args.debug, 
            n_shapes=args.n_shapes_attack_BPDA, max_steps=args.max_steps_attack,
            type_primitive=args.type_primitive_attack_BPDA,
            tmp_index=args.start, tmp_dir=args.primitive_tmp_dir,
            early_stop=args.early_stop, unbound=args.unbound) 
    elif args.attack=='PGD':
        attack = PGD(sess, model, model.threat_model.epsilon, debug=args.debug,
            max_steps=args.max_steps_attack, early_stop=args.early_stop)
    elif args.attack=='none':
        attack = NA(sess, model, model.threat_model.epsilon, debug=args.debug)

    # initialize a data provider for ImageNet images
    provider = robustml.provider.ImageNet_val_1k(args.imagenet_path, model.dataset.shape, tag, args.start, args.n_snapshot)

    success_rate = robustml.evaluate.evaluate(
        model,
        attack,
        provider,
        start=args.start,
        end=args.end,
        deterministic=True,
        debug=args.debug,
        snapshot_adv=args.snapshot_adv # save
    )

    print('attack success rate: %.2f%% (over %d data points)' % (success_rate*100, args.end-args.start))

if __name__ == '__main__':
    main()
