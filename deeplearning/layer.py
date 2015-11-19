import numpy as np

import theano
import theano.tensor as T
from Modul5.deeplearning import mnist_basics as mnist
#TODO: Experiment with  different configurations
#TODO: Add different activation functions
#TODO: Some properties might need to be changed after ANN is created the first time. Make them available
#TODO: Make it possible to change learning rate after creation off ANN
#TODO: ann.blindtest()for assignment


class HiddenLayer(object):
    def __init__(self, input, num_in, number_of_nodes, activation):
        self.num_in = num_in
        self.number_of_nodes = number_of_nodes
        self.weights = theano.shared(value=np.random.randn(num_in, number_of_nodes), name='weights') # Different initialization based on activation fn

        self.output = activation(T.dot(input, self.weights))
        self.params = [self.weights]


class ANN(object):
    def __init__(self, input, num_in, hidden_list, num_out):
        self.input = input
        self.layers = []
        self.params = []
        self.epochs = 0

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

    X = T.dmatrix("X")
    Y = T.dmatrix("Y") #vector?

    def sgd(cost, params, lr):
        gradients = [T.grad(cost=cost, wrt=param) for param in params]
        updates = [
            (param, param - lr * gradient)
            for param, gradient in zip(params, gradients)
        ]
        return updates


    ann = ANN(X, num_in, hidden, num_out)
    cost = T.sum(pow((Y -ann.layers[-1].output ), 2))
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



minibatch_size = 20


def load_train_set():
    print("Loading training cases...")
    global train_set_x
    global train_set_y
    train_set_x,train_set_y = mnist.gen_flat_cases()
    scale(train_set_x)

def build_model(hidden=[15],learning_rate=0.01):
    print("Building the model...")
    global train
    global predict
    train, predict = compile_model(28*28, hidden, 10, learning_rate)


def train_model(epochs=10):
    print("Training...")
    for i in range(epochs):
        print ("Epoch: "+ str(i))
        error = 0
        no_correct = 0
        no_false = 0
        total = 0
        for image, label in zip(train_set_x, train_set_y):
            if predict([train_set_x[i]]) == train_set_y[i]:
                no_correct +=1
            else:
                no_false+=1
            total+=1


            desired= [0 for x in range(10)]
            desired[label] = 1
            error += train([image], [desired])
        print (error/len(train_set_x))


def test_model():
    test_set_x, test_set_y = mnist.gen_flat_cases(type="testing")
    scale(test_set_x)
    no_correct=0
    no_false=0
    total=0
    for j in range(len(test_set_x)):

        prediction =predict([test_set_x[j]])
        if prediction == test_set_y[j]:

            no_correct +=1
        else:
            no_false+=1
        total+=1

    print("Correct: "+ str(no_correct))
    print("Wrong:  "+ str(no_false))
    print("Total: "+ str(total))
    print("Percentage: "+ str ((no_correct/total)*100))


while True:
    print("Commands:\n"
          "'ltr' to load training cases\n"
          "'b' to build model\n"
          "'tr' to train\n"
          "'te' to test\n")
    command = input("Type an input: \n")
    if command =='ltr':
        load_train_set()
        print('Done\n')
    elif command == 'b':
        command = int(input("How many hidden layers?: "))
        hidden = []
        for i in range(command):
            hidden.append(int(input(("How many nodes in layer "+str(i)+"?: "))))
        learning_rate = float(input("What learning rate do you want to use?: "))
        build_model(hidden,learning_rate)
        trained = 0
        print('Done\n')
    elif command == 'tr':
        command = int(input ("How many epochs do you want to train?: "))
        trained +=command
        print("Training for "+str(command)+" epochs")
        train_model(command)

        print('Done, total epochs trained: '+ str(trained)+ '\n')
    elif command == 'te':
        test_model()
        print('Done\n')


