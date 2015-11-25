"""class HiddenLayer(object):
    def __init__(self, input, n_in, n_out, activation=T.tanh):

        self.input = input

        rng = np.random.RandomState(1234)
        weights = np.asarray(
            rng.uniform(
                low=-np.sqrt(6. / (n_in + n_out)),
                high=np.sqrt(6. / (n_in + n_out)),
                size=(n_in, n_out)
            ),
            dtype=theano.config.floatX
        )<
        if activation == T.nnet.sigmoid:
            weights *= 4

        bias = np.zeros((n_out,), dtype=theano.config.floatX)

        self.W = theano.shared(value=weights, name="W", borrow=True)
        self.b = theano.shared(value=bias, name="b", borrow=True)
        self.output = activation(T.dot(input, self.W) + self.b)
        self.params = [self.W, self.b]


class SoftmaxLayer(object):
    # A SoftmaxLayer is the output layer of the network
    def __init__(self, input, n_in, n_out):
        self.input = input

        weights = np.zeros((n_in, n_out), dtype=theano.config.floatX)
        bias = np.zeros((n_out,), dtype=theano.config.floatX)

        self.W = theano.shared(value=weights, name="W", borrow=True)
        self.b = theano.shared(value=bias, name="b", borrow=True)
        self.output = T.nnet.softmax(T.dot(input, self.W) + self.b)
        self.prediction = T.argmax(self.output, axis=1)
        self.params = [self.W, self.b]

    def negative_log_likelihood(self, y):
        return -T.mean(T.log(self.output)[T.arange(y.shape[0]), y])

    def errors(self, y):
        if y.ndim != self.prediction.ndim:
            raise TypeError(
                'y should have the same shape as self.y_pred',
                ('y', y.type, 'y_pred', self.prediction.type)
            )
        # check if y is of the correct datatype
        if y.dtype.startswith('int'):
            # the T.neq operator returns a vector of 0s and 1s, where 1
            # represents a mistake in prediction
            return T.mean(T.neq(self.prediction, y))
        else:
            raise NotImplementedError()"""