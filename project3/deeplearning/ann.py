import os, sys, timeit
import numpy as np
import theano
import theano.tensor as T
from deeplearning.layer import HiddenLayer, SoftmaxLayer


class ANN(object):
    def __init__(self, input, n_in, n_hidden, n_out):

        self.input = input
        self.hidden_layers = []
        self.params = []

        for i in range(len(n_hidden)):
            self.hidden_layers.append(
                HiddenLayer(
                    input=input,
                    n_in=n_in if i == 0 else n_hidden[i-1],
                    n_out=n_hidden[i],
                    activation=T.tanh
                )
            )

        self.output_layer = SoftmaxLayer(
            input=self.hidden_layers[-1].output,
            n_in=n_hidden[-1],
            n_out=n_out
        )

        self.negative_log_likelihood = self.output_layer.negative_log_likelihood
        self.errors = self.output_layer.errors
        self.params = [hidden.params for hidden in self.hidden_layers] + self.output_layer.params

