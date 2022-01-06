import sys
import numpy as np
import pandas as pd
import pickle
import os

import cv2
import time

import tensorflow as tf
from keras.models import Sequential
import operator
from keras.optimizers import Adam
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model

from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import Concatenate
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform

from keras.engine.topology import Layer
from keras.regularizers import l2
from keras import backend as K

from sklearn.utils import shuffle

import numpy.random as rng

def read_img(path):
    image = cv2.imread(path)
    image = cv2.resize(image, (96, 96))
    image = image.reshape(1,96,96,3)
    return image

def initialize_weights(shape, dtype=None):
    return np.random.normal(loc = 0.0, scale = 1e-2, size = shape)

def initialize_bias(shape, dtype=None):
    return np.random.normal(loc = 0.5, scale = 1e-2, size = shape)


def get_siamese_model(input_shape):
    """
        Model architecture based on the one provided in: http://www.cs.utoronto.ca/~gkoch/files/msc-thesis.pdf
    """

    # Define the tensors for the two input images
    left_input = Input(input_shape)
    right_input = Input(input_shape)

    vgg16 = tf.keras.applications.VGG16(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet")
    vgg16.trainable = False

    flatten_layer = tf.keras.layers.Flatten()
    dense_layer = tf.keras.layers.Dense(256, activation='relu')
    dropout_1 = tf.keras.layers.Dropout(.2, input_shape=(2,))
    batch_1 = tf.keras.layers.BatchNormalization()
    dense_layer_2 = tf.keras.layers.Dense(256, activation='relu')
    dropout_2 = tf.keras.layers.Dropout(.2, input_shape=(2,))
    batch_2 = tf.keras.layers.BatchNormalization()
    dense_layer_3 = tf.keras.layers.Dense(256)

    vgg16_model = tf.keras.Sequential([
        vgg16,
        flatten_layer,
        dense_layer,
        dropout_1,
        batch_1,
        dense_layer_2,
        dropout_2,
        batch_2,
        dense_layer_3
    ])

    # Generate the encodings (feature vectors) for the two images
    encoded_l = vgg16_model(left_input)
    encoded_r = vgg16_model(right_input)

    # Add a customized layer to compute the absolute difference between the encodings
    L1_layer = Lambda(lambda tensors: K.abs(tensors[0] - tensors[1]))
    L1_distance = L1_layer([encoded_l, encoded_r])

    # Add a dense layer with a sigmoid unit to generate the similarity score
    prediction = Dense(1, activation='sigmoid', bias_initializer=initialize_bias)(L1_distance)

    # Connect the inputs with the outputs
    siamese_net = Model(inputs=[left_input, right_input], outputs=prediction)

    # return the model
    return siamese_net

def main():
    model = get_siamese_model((96, 96, 3))
    model.summary()
    optimizer = Adam(lr=0.00001)
    model.compile(loss="binary_crossentropy", optimizer=optimizer)
    model.load_weights(os.path.join(r"C:\Users\sriba\Documents\Python Scripts\Siamese\OneShotDocClassification\weights_vgg","weights.14000.h5"))

    base = r"C:\Users\sriba\Documents\Python Scripts\Siamese\OneShotDocClassification\val_data\new"
    train = os.path.join(base, "train")
    test = os.path.join(base, "test")

    data_dic = {}
    for category in os.listdir(train):
        category_path = os.path.join(train, category)
        data = []
        for file in os.listdir(category_path):
            img = read_img(os.path.join(category_path, file))
            data.append(img)
        data_dic[category] = data

    pair = []
    for category in os.listdir(test):
        print("Folder", category)
        category_path = os.path.join(test, category)
        print(len(os.listdir(category_path)))
        for file in os.listdir(category_path):
            img = read_img(os.path.join(category_path, file))
            cat_result = {}
            for key in data_dic:
                # print(key)
                predict_result = []
                train_data = data_dic[key]
                for data in train_data:
                    result = model.predict([data, img])
                    predict_result.append(result[0][0])
                # print(result)
                cat_result[key] = max(predict_result)
                predicted = max(cat_result.items(), key=operator.itemgetter(1))[0]
            print(predicted, cat_result[predicted])
            # print(cat_result)

main()