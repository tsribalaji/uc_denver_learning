import tensorflow as tf
from keras.models import Sequential
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
import numpy as np

class SiameseModel:
    def initialize_weights(self,shape, dtype=None):
        return np.random.normal(loc = 0.0, scale = 1e-2, size = shape)
    
    def initialize_bias(self,shape, dtype=None):
        return np.random.normal(loc = 0.5, scale = 1e-2, size = shape)

    def get_base_model(self,input_shape):
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

        return vgg16_model

    def build_siamese_model(self,input_shape):

        vgg16_model = self.get_base_model(input_shape)

        left_input = Input(input_shape)
        right_input = Input(input_shape)
        
        # Generate the encodings (feature vectors) for the two images
        encoded_l = vgg16_model(left_input)
        encoded_r = vgg16_model(right_input)
        
        # Add a customized layer to compute the absolute difference between the encodings
        L1_layer = Lambda(lambda tensors:K.abs(tensors[0] - tensors[1]))
        L1_distance = L1_layer([encoded_l, encoded_r])
        
        # Add a dense layer with a sigmoid unit to generate the similarity score
        prediction = Dense(1,activation='sigmoid',bias_initializer=self.initialize_bias)(L1_distance)
        
        # Connect the inputs with the outputs
        siamese_net = Model(inputs=[left_input,right_input],outputs=prediction)
        
        # return the model
        return siamese_net

    def get_model(self, input_shape):
        model = self.build_siamese_model(input_shape)
        optimizer = Adam(lr = 0.0001)
        model.compile(loss="binary_crossentropy",optimizer=optimizer)
        print((model.summary()))
        return model

