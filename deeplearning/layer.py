import numpy as np
import theano
import theano.tensor as T


class HiddenLayer(object):
    def __init__(self, input, num_in, number_of_nodes, activation):
        self.num_in = num_in
        self.number_of_nodes = number_of_nodes

        self.weights = self.init_weights(activation)
        self.output = activation(T.dot(input, self.weights))
        self.params = [self.weights]

    def init_weights(self, activation):
        rng = np.random.RandomState(1234)

        # Default for activation function tanh
        weights = np.asarray(
            rng.uniform(
                low=-np.sqrt(6. / (self.num_in + self.number_of_nodes)),
                high=np.sqrt(6. / (self.num_in + self.number_of_nodes)),
                size=(self.num_in, self.number_of_nodes)
            ),
            dtype=theano.config.floatX
        )

        if activation == T.nnet.sigmoid:
            weights *= 4
        elif activation == T.nnet.softmax:
            weights = np.zeros((self.num_in, self.number_of_nodes), dtype=theano.config.floatX)
        #TODO: elif activation == T.nnet.relu - find optimal weight initialization for relus

        return theano.shared(value=weights, name='weights', borrow=True)


