import numpy as np
import theano
import theano.tensor as T


class HiddenLayer(object):
    def __init__(self, input, num_in, number_of_nodes, activation):
        """
        A hidden layer in an artifical neural network is defined by the output of the activation
        function of the previous layer, the number of incoming neurons connected
        to the layer, the amount of neurons in the layer and an activation function.

        :param input: the output of the activation function in the previous layer

        :param num_in: the number of neurons in the previous layer

        :param number_of_nodes: the number of neurons in this layer

        :param activation: either hyperbolic tangent, sigmoid, rectified linear units or softmax

        :return: a HiddenLayer object to be used in an ANN object
        """

        self.num_in = num_in
        self.number_of_nodes = number_of_nodes

        self.weights = self.init_weights(activation)
        self.output = activation(T.dot(input, self.weights))
        self.params = [self.weights]

    def init_weights(self, activation):
        """
        The weights of a neural network should be initialised based on the activation function used, such that each
        neuron operates in a regime of its activation function where information can easily be propagated forwards
        and backwards early in the training stages. We draw a uniformly sampled weights using Xavier initialization
        for hyperbolic tangent and sigmoid, and simply from a range [0.0, 0.1] for rectified linear units. For softmax,
        all weights are initialized to zeroes.

        :param activation: hyperbolic tangent, sigmoid, rectified linear units or softmax

        :return: The proper uniformly sampled weights best suited for the activation function
        """

        # Default for activation function tanh
        weights = np.asarray(
            np.random.uniform(
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
        elif activation == T.nnet.relu:
            weights = np.random.uniform(low=0.0, high=0.1, size=(self.num_in, self.number_of_nodes))

        return theano.shared(value=weights, name='weights', borrow=True)


