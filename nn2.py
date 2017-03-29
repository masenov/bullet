import tensorflow as tf
import numpy as np
from api import *
from time import gmtime, strftime

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def init_weights(shape, name):
    return tf.Variable(tf.random_normal(shape, stddev=0.01), name=name)

# This network is the same as the previous one except with an extra hidden layer + dropout
def model(X, w_h, w_h2, w_o, p_keep_input, p_keep_hidden):
    # Add layer name scopes for better graph visualization
    with tf.name_scope("layer1"):
        X = tf.nn.dropout(X, p_keep_input)
        h = tf.nn.sigmoid(tf.matmul(X, w_h))
    with tf.name_scope("layer2"):
        h = tf.nn.dropout(h, p_keep_hidden)
        h2 = tf.nn.sigmoid(tf.matmul(h, w_h2))
    with tf.name_scope("layer3"):
        h2 = tf.nn.dropout(h2, p_keep_hidden)
        return tf.matmul(h2, w_o)


sess = tf.InteractiveSession()
data = seqData()
train_data = data[0:9000,:]
#train_data = train_data.reshape(train_data.shape[0]*train_data.shape[1],train_data.shape[2])
test_data = data[9000:,:]
#test_data = test_data.reshape(test_data.shape[0]*test_data.shape[1],test_data.shape[2])

trX = train_data[:,0:34]
trY = train_data[:,34:]
teX = test_data[:,0:34]
teY = test_data[:,34:]

print ("Loaded data")

X = tf.placeholder(tf.float32, shape=[None, 34])
Y = tf.placeholder(tf.float32, shape=[None, 3])

# Weights and biases of our model
W1 = weight_variable([34,100])
b1 = bias_variable([100])

# Build a regression model
h1 = tf.nn.sigmoid(tf.matmul(X,W1) + b1)

W2 = weight_variable([100,3])
b2 = bias_variable([3])

y = tf.nn.sigmoid(tf.matmul(h1,W2) + b2)

#Step 4 - Add histogram summaries for weights
tf.summary.histogram("W1", W1)
tf.summary.histogram("b1", b1)
tf.summary.histogram("h1", h1)
tf.summary.histogram("W2", W2)
tf.summary.histogram("b2", b2)
tf.summary.histogram("y", y)

# Build an error function
cross_entropy = tf.reduce_mean(tf.square(Y - y))
tf.summary.scalar("cost", cross_entropy)

# Initialize the variables
sess.run(tf.global_variables_initializer())

# Train the model with steepest gradient descent
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# Evaluate the model
correct_prediction = tf.equal(y, Y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# Step 10 create a log writer. run 'tensorboard --logdir=./logs/nn_logs'
writer = tf.summary.FileWriter("./logs/nn_logs/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()), sess.graph) # for 0.8
merged = tf.summary.merge_all()


for i in range(20):
    train_accuracy = accuracy.eval(feed_dict={
            X:trX, Y: trY})
    print("step %d, training accuracy %g"%(i, train_accuracy))
    train_step.run(feed_dict={X: trX, Y: trY})



print(accuracy.eval(feed_dict={X: teX, Y: teY}))
