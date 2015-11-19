import time

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


class ANN(object):
    def __init__(self, input, num_in, hidden_list, act_list, num_out):
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


def compile_model(num_in, hidden, activations, num_out, learning_rate):

    X = T.dmatrix("X")
    Y = T.dmatrix("Y")

    def sgd(cost, params, lr):
        gradients = [T.grad(cost=cost, wrt=param) for param in params]
        updates = [
            (param, param - lr * gradient)
            for param, gradient in zip(params, gradients)
        ]
        return updates


    ann = ANN(X, num_in, hidden, activations, num_out)
    cost = T.sum(pow((Y - ann.layers[-1].output), 2))
    # cost = T.nnet.categorical_crossentropy(ann.layers[-1].output, Y).mean()
    updates = sgd(cost=cost, params=ann.params, lr=learning_rate)
    Y_pred = T.argmax(ann.layers[-1].output, axis=1)

    train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
    predict = theano.function(inputs=[X], outputs=Y_pred, allow_input_downcast=True)

    return train, predict


def scale(images):
    for image in range(len(images)):
        for value in range(len(images[image])):
            images[image][value] /= 255.0


def load_train_set():
    print("Loading training cases...")
    global train_set_x
    global train_set_y
    train_set_x,train_set_y = mnist.gen_flat_cases()
    scale(train_set_x)
    global total_time
    total_time = 0

def build_model(hidden, activations, learning_rate):
    print("Building the model...")
    global train
    global predict
    train, predict = compile_model(28*28, hidden, activations, 10, learning_rate)


def train_model(epochs=10, bulk=False, bulk_size=250):
    starttime = time.time()
    for i in range(epochs):
        print("epoch: ", i)
        error = 0
        i = 0
        j = bulk_size
        while j < len(train_set_x):
            image_bulk = train_set_x[i:j]
            # Creating a result bulk with only zeros
            result_bulk = [[0 for i in range(10)] for i in range(bulk_size)]
            for k in range(bulk_size):
                label_index = train_set_y[i + k]
                result_bulk[k][label_index] = 1
            i += bulk_size
            j += bulk_size
            # Provide some feedback while processing images
            if j % (bulk_size * 100) == 0:
                print("image nr: ", j)
            error += train(image_bulk, result_bulk)
        print("avg error pr image: " + str(error/j))

    # if bulk:
    #     print("Training with bulk size "+ str(bulk_size))
    # else:
    #     print("Training...")
    #
    # for i in range(epochs):
    #     print ("Epoch: "+ str(i))
    #     error = 0
    #     no_correct = 0
    #     no_false = 0
    #     total = 0
    #     if bulk:
    #         start= 0
    #         end = start + bulk_size
    #         train_subset_x = train_set_x[start:end]
    #         train_subset_y = train_set_y[start:end]
    #     else:
    #         train_subset_x = train_set_x
    #         train_subset_y = train_set_y
    #
    #     if bulk:
    #         while end < len(train_set_x):
    #             for image, label in zip(train_subset_x, train_subset_y):
    #                 if predict([image]) == label:
    #                     no_correct += 1
    #                 else:
    #                     no_false += 1
    #                 total += 1
    #                 desired = [0 for x in range(10)]
    #                 desired[label] = 1
    #                 error += train(train_subset_x, train_subset_y)
    #             start = end
    #             end += bulk_size
    #             train_subset_x = train_set_x[start:end]
    #             train_subset_y = train_set_y[start:end]
    #
    #         print (error/len(train_set_x))
    #
    #     else:
    #         for image, label in zip(train_subset_x, train_subset_y):
    #                 if predict([image]) == label:
    #                     no_correct += 1
    #                 else:
    #                     no_false += 1
    #
    #         total += 1
    #         desired= [0 for x in range(10)]
    #         desired[label] = 1
    #         error += train([image], [desired])
    #         print (error/len(train_subset_x))



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
    return (no_correct/total)*100

def activation_map(x):
    return {
        0: T.tanh,
        1: T.nnet.sigmoid,
        2: T.nnet.relu,
        3: T.nnet.softmax,
    }.get(x, T.tanh) # T.tanh is default if x is not found

while True:

    print("Commands:\n"
          "'l' to load training cases\n"
          "'b' to build model\n"
          "'tr' to train\n"
          "'te' to test\n")
    command = input("Type an input: \n")
    if command == 'l':
        load_train_set()
        print('Done.\n')
    elif command == 'b':
        print("Please specify a topology description on the form: 40,20,60")
        hidden = [x for x in map(int, input("Topology: ").strip().split(","))]

        print("\nPlease specify activation functions for each layer on the form: 0,2,1")
        print("0: hyperbolic tangent, 1: sigmoid, 2: rectified linear unit, 3: softmax")
        activations = [activation_map(x) for x in list(map(int, input("Activations: ").strip().split(",")))]

        learning_rate = float(input("\nWhat learning rate do you want to use?: "))
        total_time = 0
        build_model(hidden, activations, learning_rate)
        trained = 0
        print('Done\n')
    elif command == 'tr':
        command = int(input("How many epochs do you want to train?: "))
        trained +=command
        print("Training for "+str(command)+" epochs")
        t = time.time()
        train_model(command, bulk=True, bulk_size=25)
        el = time.time() -t
        total_time +=el

        print('Done, total epochs trained: '+ str(trained)+ '\n')
    elif command == 'te':
        percentage = test_model()
        f = open('statistics','a')
        f.write("Configuration:\n"
                "Hidden layers and nodes: "+ repr(hidden)+"\n"+
                "Learning rate: "+ str(learning_rate)+ "\n"+
                "Epochs: "+ str(trained)+"\n"+
                "Error percentage: " + str(percentage)+"\n"+
                "Time trained: "+ str(total_time)+"\n")

        f.close()
        print('Done\n')


