# import robustml
import robustml_dev as robustml
from defense import *
from primitive import primitive_defend
from inceptionv3 import model as inceptionv3_model
import tensorflow as tf

class InputTransformations(robustml.model.Model):
    def __init__(self, sess, defense, n_shapes=200, type_primitive='1', tmp_index=1, tmp_dir='./ram'):
        self._n_shapes= n_shapes
        self._sess = sess
        self._input = tf.placeholder(tf.float32, (299, 299, 3))
        input_expanded = tf.expand_dims(self._input, axis=0)

        self._logits, _ = inceptionv3_model(sess, input_expanded)
        self._probs = tf.nn.softmax(self._logits)
        self._predictions = tf.argmax(self._probs, 1)

        self._type_primitive=type_primitive
        self._tmp_index=tmp_index
        self._tmp_dir=tmp_dir

        def identity(x, n_triangle=200, type_primitive='1', tmp_index=1, tmp_dir="./ram"): 
            '''
            Dummy identity, do nothing
            '''
            return x

        if defense == 'bitdepth':
            self._defend = defend_reduce
        elif defense == 'primitive':
            self._defend = primitive_defend
        elif defense == 'none':
            self._defend = identity
        else:
            raise ValueError('invalid defense: %s' % defense)

        self._dataset = robustml.dataset.ImageNet((299, 299, 3))
        self._threat_model = robustml.threat_model.L2(epsilon=0.05*299) # 0.05 * sqrt(299*299)

    @property
    def dataset(self):
        return self._dataset

    @property
    def threat_model(self):
        return self._threat_model

    def classify(self, x):
        x_defended = self.defend(x, self._n_shapes,
            self._type_primitive, self._tmp_index, self._tmp_dir)
        return self._sess.run(self._predictions, {self._input: x_defended})[0]

    # expose internals for white box attacks

    def defend(self, x, n_triangle, type_primitive, tmp_index, tmp_dir):
        return self._defend(x, n_triangle, type_primitive, tmp_index, tmp_dir)

    @property
    def input(self):
        return self._input

    @property
    def logits(self):
        return self._logits

    @property
    def predictions(self):
        return self._predictions
