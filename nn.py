import tensorflow as tf
import numpy as np
from api import *

sess = tf.InteractiveSession()

train_data = Data(0,30)
train_data = train_data.reshape(train_data.shape[0]*train_data.shape[1],train_data.shape[2])
x_data = train_data[:,0:7]
y_data = train_data[:,7:]

test_data = Data(30,35)
test_data = test_data.reshape(test_data.shape[0]*test_data.shape[1],test_data.shape[2])
x_test = test_data[:,0:7]
y_test = test_data[:,7:]



print (x_data.shape,y_data.shape)
x = tf.placeholder(tf.float32, shape=[None, 7])
y_ = tf.placeholder(tf.float32, shape=[None, 3])

# Weights and biases of our model
W = tf.Variable(tf.zeros([7,3]))
b = tf.Variable(tf.zeros([3]))

# Initialize the variables
sess.run(tf.global_variables_initializer())

# Build a regression model
y = tf.matmul(x,W) + b

# Build an error function
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_))

# Train the model with steepest gradient descent
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
train_step.run(feed_dict={x: x_data, y_: y_data})

# Evaluate the model
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(accuracy.eval(feed_dict={x: x_test, y_: y_test}))
u = W.eval()
print (u)
