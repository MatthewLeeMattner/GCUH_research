import tensorflow as tf
import os
import numpy as np
from data_formatter import Data_Formatter
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class NeuralNetwork:
    shape = []

    def __init__(self):
        self.self = self

    def setupModel(self, sess, shape):
        self.sess = sess
        self.shape = shape
        self.x = tf.placeholder(tf.float32, [None, self.shape[0][0]]) #Creates an input placeholder with input of 360 (signal length as 1d Array)
        self.y_ = tf.placeholder(tf.float32, [None, self.shape[-1][0]])
        self.y = self.getY(shape)

        self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=self.y))
        self.train_step = tf.train.GradientDescentOptimizer(0.1).minimize(self.cross_entropy)
        self.correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))

        sess.run(tf.global_variables_initializer())

    def getY(self, shape):
        output = self.x
        for i in range(1, len(self.shape)-1):
            output = self.hidden_layer(output, shape[i])
        return output

    def hidden_layer(self, output, layerShape):
        w = self.weight_variable(layerShape)
        b = self.bias_variable(layerShape)
        output = tf.matmul(output, w) + b
        return output

    def weight_variable(self, layerShape):
        W = tf.Variable(tf.truncated_normal(layerShape, stddev=0.1))
        return W

    def bias_variable(self, layerShape):
        b = tf.Variable(tf.constant(0.1, shape=[layerShape[1]]))
        return b



    def train(self, x, y):
        self.sess.run(self.train_step, feed_dict={self.x: x, self.y_: y})

    def test(self, x, y):
        acc = self.sess.run([self.accuracy], feed_dict={self.x: x, self.y_: y})
        print("ACCURACY", acc)

    def run(self, x):
        print(x)
        #print(sess.run([self.y], feed_dict={self.x: [0,x]}))


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

nn = NeuralNetwork()
with tf.Session() as sess:
    nn.setupModel(sess, [[360], [360, 100], [2]])
    '''
    nn.test(df.x_test, df.y_test)
    nn.train(df.x_train, df.y_train)
    nn.test(df.x_test, df.y_test)
    nn.run(df.x_test[0])
    saver = tf.train.Saver()
    saver.save(sess, "model/ann")
    '''