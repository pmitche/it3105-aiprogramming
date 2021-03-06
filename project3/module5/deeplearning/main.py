import time
import numpy as np
import theano.tensor as T
from project3.module5.basics import mnist_basics as mnist
from project3.module5.deeplearning.ann import ANN


def scale(images):
    # scale the original pixel intensities of the range [0, 255] down to a range
    # of [0.0, 1.0]
    for image in range(len(images)):
        for value in range(len(images[image])):
            images[image][value] /= 255.0


def activation_map(x):
    return {
        0: T.tanh,
        1: T.nnet.sigmoid,
        2: lambda k: T.switch(k > 0, k, 0),  # Equivalent to T.nnet.relu (rectified linear unit)
        3: T.nnet.softmax,
    }.get(x, T.tanh)  # T.tanh is default if x is not found


def train_model(epochs, minibatch_size):
    """
    Trains the neural network for x amount of epochs with a specific minibatch size.

    :param epochs:          the number of epochs for which to train the network
    :param minibatch_size:  the size of each minibatch
    :return:
    """
    for epoch in range(epochs):
        print("Training epoch number {}...".format(epoch))
        cost = 0

        for i in range(0, len(train_set_x), minibatch_size):
            image_batch = train_set_x[i:i+minibatch_size]
            label_batch = np.zeros((minibatch_size, 10), dtype=np.int)
            for k in range(minibatch_size):
                label_batch[k][train_set_y[i + k]] = 1
            cost = ann.train(image_batch, label_batch)

        print("Cost after epoch {}: {}".format(epoch, cost))


def test_model():
    """
    Tests the model on a test set and checks how many cases the network managed to classify correctly.
    :return:
    """
    correct = 0
    total = len(test_set_x)

    for i in range(total):
        prediction = ann.predict([test_set_x[i]])
        if prediction == test_set_y[i]:
            correct += 1

    print("Correct: {}".format(correct))
    print("Wrong: {}".format(total - correct))
    print("Total: {}".format(total))
    print("Percentage: {:.2%}\n".format(correct / total))


# Loading training and test cases
print("Loading training set...")
train_set_x, train_set_y = mnist.gen_flat_cases(type="training")
scale(train_set_x)
print("Finished loading training set! \n")
print("Loading test set...")
test_set_x, test_set_y = mnist.gen_flat_cases(type="testing")
scale(test_set_x)
print("Finished! Statistics:")

while True:
    # Building network
    hidden = [x for x in map(int, input("Please specify a topology description on the form 40,20,60: ").strip().split(","))]
    print("\n0: hyperbolic tangent, 1: sigmoid, 2: rectified linear unit, 3: softmax")
    activations = [activation_map(x) for x in list(map(int, input("Please specify activation functions for each layer on the form 0,2,1: ").strip().split(",")))]
    lr = float(input("What learning rate do you want to use?: "))
    print("Building model...")
    ann = ANN(28*28, hidden, activations, 10, lr)
    print("Finished building model!\n")

    # Specifying training duration and batch size
    epochs = int(input("How many epochs to you want to train?: "))
    minibatch_size = int(input("And what minibatch size do you want to use?: "))
    print("\nTraining for {} epochs with minibatch size {}...".format(epochs, minibatch_size))
    start = time.time()
    train_model(epochs, minibatch_size)
    total_time = time.time() - start
    print("Finished training! Total time used: {:.2f} seconds. \n".format(total_time))

    # Test the network
    test_model()

    if input("Want to build a different network? y/n: ") == "n":
        break