import theano
import theano.tensor as T

from Modul5.deeplearning.layer import HiddenLayer


class ANN(object):
    def __init__(self, num_in, hidden_list, act_list, num_out, learning_rate):
        self.X = T.dmatrix("X")
        self.layers = []
        self.params = []

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
            gradients = [T.grad(cost=cost, wrt=param) for param in params]
            updates = [
                (param, param - lr * gradient)
                for param, gradient in zip(params, gradients)
            ]
            return updates

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