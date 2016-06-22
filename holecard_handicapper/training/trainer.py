import os
import sys
import importlib

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from keras.callbacks import Callback
from keras.callbacks import EarlyStopping
from holecard_handicapper.training.model_tester import ModelTester
from slack.messanger import Messenger

class LossHistory(Callback):

  def on_train_begin(self, logs={}):
    self.losses = []
    self.val_losses = []

  def on_epoch_end(self, epoch, logs={}):
    self.losses.append(logs['loss'])
    self.val_losses.append(logs['val_loss'])

class SlackCallback(Callback):

  def __init__(self, slack, nb_epoch):
    self.nb_epoch = nb_epoch
    self.slack = slack
    self.checkpoint = [nb_epoch/4, nb_epoch/2, 3*nb_epoch/4]
    self.complete_rate = [0.25, 0.50, 0.75]

  def on_train_begin(self, logs={}):
    self.slack.post_message("Start training!!")

  def on_epoch_end(self, epoch, logs={}):
    if epoch in self.checkpoint:
      progress = self.complete_rate[self.checkpoint.index(epoch)]
      msg = '[Progress]\n loss=%f, val_loss=%f (%d/%d)' % (logs['loss'], logs['val_loss'], epoch, self.nb_epoch)
      log = self.slack.post_message(msg)

class Trainer:

  def __init__(self, nb_epoch, batch_size, verbose, validation_split):
    self.params = {'nb_epoch':nb_epoch, 'batch_size':batch_size, 'verbose':verbose, 'validation_split':validation_split,
        'slack': { 'use':False, 'progress': False, 'result': False} }

  def use_slack(self, token, progress=True, result=True):
    self.params['slack']['use'] = True
    self.params['slack']['progress'] = progress
    self.params['slack']['result'] = result
    self.slack = Messenger(token, '#holecardhandicapper')


  def train(self, data, model_builder_path):
    (X_train, Y_train), (X_test, Y_test) = data
    model = self.__gen_model(model_builder_path)
    callbacks = self.__gen_callbacks(True, self.params['slack']['use'], self.params['nb_epoch'])
    history = callbacks[0]
    model.fit(X_train, Y_train,
        nb_epoch=self.params['nb_epoch'], batch_size=self.params['batch_size'],
        verbose=self.params['verbose'], validation_split=self.params['validation_split'],
        callbacks=callbacks)
    score = model.evaluate(X_test, Y_test, batch_size=self.params['batch_size'])
    tester = ModelTester()
    sample_result = tester.run_popular_test_case(model)
    out_dir_path = self.__fetch_output_directory(model_builder_path)
    self.__save_result(score, sample_result, history, out_dir_path)
    self.__save_model(model, out_dir_path)


  def __gen_callbacks(self, early_stopping, slack, nb_epoch):
    callbacks = [LossHistory()]
    if early_stopping:
      callbacks.append(EarlyStopping(monitor='val_loss', patience=50, mode='min'))
    if slack:
      callbacks.append(SlackCallback(self.slack, nb_epoch))
    return callbacks

  def __fetch_output_directory(self, builder_path):
    return os.path.dirname(builder_path)

  def __gen_model(self, builder_path):
    sys.path.append(os.path.dirname(builder_path))
    file_name = os.path.basename(builder_path)
    m = importlib.import_module(os.path.splitext(file_name)[0])
    builder = m.ModelBuilder()
    return builder.build()

  def __save_result(self, score, sample_result, history, directory_path):
    X = np.arange(len(history.losses))
    plt.plot(X, history.losses, 'r', alpha=0.5, label='loss')
    plt.plot(X, history.val_losses, 'b', alpha=0.5, label='val_loss')
    plt.legend()
    img_path = os.path.join(directory_path, 'loss_graph.png')
    plt.savefig(img_path)
    with open(os.path.join(directory_path, 'result.txt'), 'w') as f:
      result = "loss on test = %f\n\n" % score
      f.write(result+sample_result)
      if self.params['slack']['result']:
        self.slack.post_image(img_path)
        self.slack.post_message("[RESULT] "+ result + sample_result)

  def __save_model(self, model, directory_path):
    model_json = model.to_json()
    with open(os.path.join(directory_path, 'model_arrchitecture.json'), 'w') as f:
      f.write(model_json)
    model.save_weights(os.path.join(directory_path, 'model_weights.h5'), overwrite=True)

