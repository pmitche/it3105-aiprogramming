# IT3105 Artificial Intelligence Programming - Module 5
This directory contains deliverables for the 5th module in the course IT3105 AI programming at the Norwegian University of Science and Technology. 

### Usage
Download and unzip the [zip file of MNIST images and code](http://www.idi.ntnu.no/emner/it3105/assignments/data/ann/mnist.zip), and place the basics folder in the root of this directory. Remember to modify the path in mnist_basics.py

Our best-performing neural network managed to classify 9858 test images correctly out of 10000 total. We used cross-entropy as our cost function in the stochastic gradient descent algorithm, two hidden layers of size 800 and 400, both using rectified linear units as their activation functions, and a learning rate of 0.01. We trained it on the entire MNIST training set of 60000 training images over the course of 30 epochs with minibatches of size 25. Total time trained was 7 minutes and 40 seconds. 
