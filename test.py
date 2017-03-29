import tensorflow as tf
import csv
import numpy as np
from tempfile import TemporaryFile


with open('test.txt', 'w') as fout:
                    fout.writelines("")
num_lines = sum(1 for line in open('data.txt'))
print (num_lines)
with open('data.txt', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print (len(row))
        break


session = tf.InteractiveSession()
x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)
bias = tf.Variable(1.0)
y_pred = x ** 2 + bias     # x -> x^2 + bias
loss = (y - y_pred)**2     # l2 loss?

session.run(tf.global_variables_initializer())

# Error: to compute loss, y is required as a dependency
# print('Loss(x,y) = %.3f' % session.run(loss, {x: 3.0}))
# OK, print 1.000 = (3**2 + 1 - 9)**2
print('Loss(x,y) = %.3f' % session.run(loss, {x: 3.0, y: 9.0}))
# OK, print 10.000; for evaluating y_pred only, input to y is not required
print('pred_y(x) = %.3f' % session.run(y_pred, {x: 3.0}))
# OK, print 1.000 bias evaluates to 1.0
print('bias      = %.3f' % session.run(bias))


outfile = TemporaryFile()
x = np.arange(10)
#np.save('data.npy', x)

y = np.load('data.npy')
print (y)
