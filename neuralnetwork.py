import tensorflow as tf
import os
import numpy as np
from data_formatter import Data_Formatter
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class NeuralNetwork:
    shape = []

    def __init__(self, shape):
        self.shape = shape
        self.x = tf.placeholder(tf.float32, [None, self.shape[0]]) #Creates an input placeholder with input of 360 (signal length as 1d Array)
        self.y_ = tf.placeholder(tf.float32, [None, self.shape[-1]])
        return

    def setupModel(self, sess):
        self.sess = sess
        self.y = self.setupHLs()
        self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=self.y))
        self.train_step = tf.train.GradientDescentOptimizer(0.1).minimize(self.cross_entropy)
        self.correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))
        sess.run(tf.global_variables_initializer())

    def setupHLs(self):
        inputValue = self.x
        for i in range(0, len(self.shape)-1):
            inputValue = self.hidden_layer(inputValue, [self.shape[i], self.shape[i+1]])
        return inputValue

    def weight_variable(self, shape):
        W = tf.Variable(tf.truncated_normal(shape, stddev=0.1))
        return W

    def bias_variable(self, shape):
        b = tf.Variable(tf.constant(0.1, shape=[shape]))
        return b

    def hidden_layer(self, inputValue, layerShape):
        w = self.weight_variable([layerShape[0], layerShape[1]])
        b = self.bias_variable(layerShape[1])
        output = tf.matmul(inputValue, w) + b
        return output

    def train(self, x, y):
        self.sess.run(self.train_step, feed_dict={self.x: x, self.y_: y})

    def test(self, x, y):
        acc = self.sess.run([self.accuracy], feed_dict={self.x: x, self.y_: y})
        print("ACCURACY", acc)

    def run(self, x):
        print(x)
        print(sess.run([self.y], feed_dict={self.x: [0,x]}))


#MAIN#######################################
print("Importing Data")
signals, labels = [], []
signals = np.load("data/features_MLII.npy")
labels = np.load("data/labels_MLII.npy")
df = Data_Formatter()

print("ct", df.countType(labels))
df.assign_data(signals, labels)
print("S, L: ", len(labels), len(signals))
print("ct", df.countType(df.y))
df.equalize_data()
print("ct", df.countType(df.y))
df.split_training_testing()
print("ytest", df.countType(df.y_test))
print("ytrain", df.countType(df.y_train))

nn = NeuralNetwork([360, 100, 2])
with tf.Session() as sess:
    nn.setupModel(sess)
    nn.test(df.x_test, df.y_test)
    nn.train(df.x_train, df.y_train)
    nn.test(df.x_test, df.y_test)
    nn.run(df.x_test[0])
