import numpy as np
from time import time
import theano
import theano.tensor as T
from deeplearning import mnist_basics as mnist


class HiddenLayer(object):
    def __init__(self, input, num_in, number_of_nodes, activation):

        self.num_in = num_in
        self.number_of_nodes = number_of_nodes

        self.weights = theano.shared(value=np.random.randn(num_in, number_of_nodes), name='weights') # Different initialization based on activation fn
        self.bias = theano.shared(value=np.random.randn(number_of_nodes, 1), name='bias')
        self.output = activation(T.dot(input, self.weights) + self.bias)
        self.params = [self.weights, self.bias]


class ANN(object):
    def __init__(self, input, num_in, hidden_list, num_out):
        self.input = input
        self.layers = []
        self.params = []

        for i in range(len(hidden_list)):
            self.layers.append(
                HiddenLayer(
                    input=input if i == 0 else self.layers[i-1].output,
                    num_in=num_in if i == 0 else self.layers[i-1].number_of_nodes,
                    number_of_nodes=hidden_list[i],
                    activation=T.tanh
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


def compile_model(num_in, hidden, num_out, learning_rate):

    X = T.fmatrix("X")
    Y = T.fmatrix("Y") #vector?

    def sgd(cost, params, lr):
        gradients = [T.grad(cost=cost, wrt=param) for param in params]
        updates = [
            (param, param - lr * gradient)
            for param, gradient in zip(params, gradients)
        ]
        return updates


    ann = ANN(X, num_in, hidden, num_out)
    cost = T.sum(pow((Y - ann.layers[-1].output), 2))
    #cost = T.nnet.categorical_crossentropy(ann.layers[-1].output, Y).mean()
    updates = sgd(cost=cost, params=ann.params, lr=learning_rate)
    Y_pred = T.argmax(ann.layers[-1].output, axis=1)

    train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
    predict = theano.function(inputs=[X], outputs=Y_pred, allow_input_downcast=True)

    return train, predict


def scale(images):
    for image in range(len(images)):
        for value in range(len(images[image])):
            images[image][value] /= 255.0

learning_rate = 0.05
epochs = 400
hidden = [300, 200]
minibatch_size = 20

print("Loading training cases...")
train_set_x, train_set_y = mnist.gen_flat_cases()
scale(train_set_x)

print("Building the model...")
train, predict = compile_model(28*28, hidden, 10, learning_rate)

print("Training...")
#for images, labels in zip(train_set_x, train_set_y):
#    train(images, labels)