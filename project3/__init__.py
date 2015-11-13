__author__ = 'sondredyvik'
import theano
from theano import tensor

a = tensor.dscalar()
b = tensor.dscalar()

c = a +b

f = theano.function([a,b],c)
assert 4.0==f(1.5,2.5)