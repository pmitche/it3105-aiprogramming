import theano
import theano.tensor as T

from Modul5.deeplearning.layer import HiddenLayer


class ANN(object):
    def __init__(self, num_in, hidden_list, act_list, num_out, learning_rate):
        """
        An Artifical Neural Network (ANN) is defined by the number of nodes in its input layer (which, for MNIST
        classification will be 784), the number of hidden layers, the number of neurons in each hidden layer,
        the preferred activation function for each hidden layer, and the number of neurons in its output layer (which,
        for MNIST classification will be 10, corresponding to the digits 0-9. In addition, when creating an ANN object,
        we also pass in a learning rate such that we can compile a Theano model during initialization, with the learning
        rate passed into its stochastic gradient descent method.

        :param num_in:          the amount of neurons in the input layer

        :param hidden_list:     a list of the amount of neurons in each hidden layer, where value K at index i says that
                                there should be K neurons in hidden layer i

        :param act_list:        a list of activation functions for each hidden layer, where value K at index i says that
                                layer i should use activation function K

        :param num_out:         the amount of neurons in the output layer

        :param learning_rate:   the float value that is passed in to the models stochastic gradient descent
                                method

        :return:                two Theano functions, train and predict, where train returns the cost but at the same
                                time updates the networks weights based on the stochastic gradient descent algorithm,
                                and predict simply calculates the errors that are made by the model
        """

        self.X = T.dmatrix("X")
        self.layers = []
        self.params = []

        # The first hidden layer has the amount of neurons in the input layer connected to it, while all subsequent
        # layers have the amount of neurons in the previous layer connected to it.
        for i in range(len(hidden_list)):
            self.layers.append(
                HiddenLayer(
                    input=self.X if i == 0 else self.layers[i-1].output,
                    num_in=num_in if i == 0 else self.layers[i-1].number_of_nodes,
                    number_of_nodes=hidden_list[i],
                    activation=act_list[i]
                )
            )
            self.params += self.layers[i].params

        # Output layer should always be a SoftmaxLayer.
        self.layers.append(
            HiddenLayer(
                input=self.layers[-1].output,
                num_in=self.layers[-1].number_of_nodes,
                number_of_nodes=num_out,
                activation=T.nnet.softmax
            )
        )
        self.params += self.layers[-1].params

        self.train, self.predict = self.compile_model(self.X, self.layers, self.params, learning_rate)

    def compile_model(self, X, layers, params, learning_rate):

        Y = T.dmatrix("Y")

        def sgd(cost, params, lr):
            """
            The stochastic gradient descent algorithm calculates the gradient of the cost function with respect
            to all the weights in the network, and uses this gradient to update the networks weights in an attempt
            to minimize the cost function.

            :param cost:    either the sum of squared errors, or categorical cross-entropy

            :param params:  the weights in the network

            :param lr:      a float value used as a factor for the stochastic gradient

            :return:        two Theano functions, train and predict, to be used for training and testing respectively
            """
            gradients = [T.grad(cost=cost, wrt=param) for param in params]
            updates = [
                (param, param - lr * gradient)
                for param, gradient in zip(params, gradients)
            ]
            return updates

        # the cost we minimize during training is either the sum of squared errors, or the
        # categorical cross entropy, depending upon what the architecture of the neural network is.
        cost = T.sum(pow((Y - layers[-1].output), 2))
        # cost = T.nnet.categorical_crossentropy(ann.layers[-1].output, Y).mean()

        updates = sgd(cost=cost, params=params, lr=learning_rate)
        Y_pred = T.argmax(layers[-1].output, axis=1)

        train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
        predict = theano.function(inputs=[X], outputs=Y_pred, allow_input_downcast=True)

        return train, predict

    def blind_test(self, images):

        def scale(images):
            for image in range(len(images)):
                for value in range(len(images[image])):
                    images[image][value] /= 255.0

        scale(images)
        predictions = []
        for image in images:
            predictions.append(self.predict([image]))
        return predictions