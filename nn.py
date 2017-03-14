import tensorflow as tf
import numpy as np
from api import *

# def weight_variable(shape):
#   initial = tf.truncated_normal(shape, stddev=0.1)
#   return tf.Variable(initial)

# def bias_variable(shape):
#   initial = tf.constant(0.1, shape=shape)
#   return tf.Variable(initial)

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

train_data = Data(0,900)
train_data = train_data.reshape(train_data.shape[0]*train_data.shape[1],train_data.shape[2])
test_data = Data(200,300)
test_data = test_data.reshape(test_data.shape[0]*test_data.shape[1],test_data.shape[2])

trX = train_data[:,0:7]
trY = train_data[:,7:]
teX = test_data[:,0:7]
teY = test_data[:,7:]

print ("Loaded data")

X = tf.placeholder(tf.float32, shape=[None, 7])
Y = tf.placeholder(tf.float32, shape=[None, 3])

#Step 3 - Initialize weights
w_h = init_weights([7, 625], "w_h")
w_h2 = init_weights([625, 625], "w_h2")
w_o = init_weights([625, 3], "w_o")

#Step 4 - Add histogram summaries for weights
tf.summary.histogram("w_h_summ", w_h)
tf.summary.histogram("w_h2_summ", w_h2)
tf.summary.histogram("w_o_summ", w_o)

#Step 5 - Add dropout to input and hidden layers
p_keep_input = tf.placeholder("float", name="p_keep_input")
p_keep_hidden = tf.placeholder("float", name="p_keep_hidden")

#Step 6 - Create Model
py_x = model(X, w_h, w_h2, w_o, p_keep_input, p_keep_hidden)

#Step 7 Create cost function
with tf.name_scope("cost"):
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=py_x, labels=Y))
    train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)
    # Add scalar summary for cost tensor
    tf.summary.scalar("cost", cost)


#Step 8 Measure accuracy
with tf.name_scope("accuracy"):
    correct_pred = tf.equal(tf.argmax(Y, 1), tf.argmax(py_x, 1)) # Count correct predictions
    acc_op = tf.reduce_mean(tf.cast(correct_pred, "float")) # Cast boolean to float to average
    # Add scalar summary for accuracy tensor
    tf.summary.scalar("accuracy", acc_op)

#Step 9 Create a session
with tf.Session() as sess:
    # Step 10 create a log writer. run 'tensorboard --logdir=./logs/nn_logs'
    writer = tf.summary.FileWriter("./logs/nn_logs", sess.graph) # for 0.8
    merged = tf.summary.merge_all()

    # Step 11 you need to initialize all variables
    tf.global_variables_initializer().run()

    #Step 12 train the  model
    for i in range(100):
        for start, end in zip(range(0, len(trX), 128), range(128, len(trX)+1, 128)):
            sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end],
                                          p_keep_input: 0.8, p_keep_hidden: 0.5})
        summary, acc = sess.run([merged, acc_op], feed_dict={X: teX, Y: teY,
                                          p_keep_input: 1.0, p_keep_hidden: 1.0})
        writer.add_summary(summary, i)  # Write summary
        print(i, acc)                   # Report the accuracy

# # Weights and biases of our model
# W1 = weight_variable([7,10])
# b1 = bias_variable([10])

# # Build a regression model
# h1 = tf.nn.relu(tf.matmul(x,W1) + b1)

# W2 = weight_variable([10,3])
# b2 = bias_variable([3])

# y = tf.nn.relu(tf.matmul(h1,W2) + b2)

# # Build an error function
# cross_entropy = tf.reduce_mean(tf.square(y - y_))

# # Initialize the variables
# sess.run(tf.global_variables_initializer())

# # Train the model with steepest gradient descent
# train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# # Evaluate the model
# correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# u = W1.eval()
# print (u)
# u2 = b1.eval()
# print (u2)
# u3 = W2.eval()
# print (u3)
# u4 = b2.eval()
# print (u4)

# for i in range(20):
#     u = W1.eval()
#     print (u)
#     u2 = b1.eval()
#     print (u2)
#     u3 = W2.eval()
#     print (u3)
#     u4 = b2.eval()
#     print (u4)
#     train_accuracy = accuracy.eval(feed_dict={
#             x:x_test, y_: y_test})
#     print("step %d, training accuracy %g"%(i, train_accuracy))
#     train_step.run(feed_dict={x: x_data, y_: y_data})


# print(accuracy.eval(feed_dict={x: x_test, y_: y_test}))
# u = W1.eval()
# print (u)
# u2 = b1.eval()
# print (u2)
# u3 = W2.eval()
# print (u3)
# u4 = b2.eval()
# print (u4)
