from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

from holecard_handicapper.model.base_model_builder import BaseModelBuilder

class ModelBuilder(BaseModelBuilder):

  def build(self):
    param = {'num_hidden_layers': 2, 'num_nodes': 100, 'activation': 'relu'}
    model = Sequential()
    for _ in range(param['num_hidden_layers']):
        model.add(Dense(param['num_nodes'], input_dim=52))
        model.add(Activation(param['activation']))
        model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(RMSprop(), 'mse')
    return model

