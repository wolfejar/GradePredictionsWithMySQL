import tensorflow as tf
from tensorflow import keras
import os


def build_model():
    model = keras.Sequential([
        keras.layers.Dense(15, activation=tf.nn.relu),
        keras.layers.Dense(20, activation=tf.nn.relu),
        keras.layers.Dense(1)
    ])
    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mean_squared_error',
                  optimizer=optimizer,
                  metrics=['mean_absolute_error', 'mean_squared_error'])
    return model


def get_model():
    model = build_model()
    if os.path.isfile('./checkpoint'):
        model.load_weights('./most_recent_model')
        return model
    else:
        return 'model not found'
