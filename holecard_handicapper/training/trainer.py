import os
import sys
import importlib
import time

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from keras.callbacks import Callback
from keras.callbacks import EarlyStopping, ModelCheckpoint
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

  def __init__(self, slack, nb_epoch, target_name):
    self.nb_epoch = nb_epoch
    self.slack = slack
    self.checkpoint = [nb_epoch/4, nb_epoch/2, 3*nb_epoch/4]
    self.complete_rate = [0.25, 0.50, 0.75]
    self.target_name = target_name

  def on_train_begin(self, logs={}):
    self.slack.post_message("Start training of [%s]!!" % self.target_name)

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
    start_time = time.time()
    (X_train, Y_train), (X_test, Y_test) = data
    model = self.__gen_model(model_builder_path)
    out_dir_path = self.__fetch_output_directory(model_builder_path)
    self.__save_model(model, out_dir_path)
    callbacks = self.__gen_callbacks(True, self.params['slack']['use'], self.params['nb_epoch'], out_dir_path)
    history = callbacks[0]
    model.fit(X_train, Y_train,
        nb_epoch=self.params['nb_epoch'], batch_size=self.params['batch_size'],
        verbose=self.params['verbose'], validation_split=self.params['validation_split'],
        callbacks=callbacks)
    score = model.evaluate(X_test, Y_test, batch_size=self.params['batch_size'])
    tester = ModelTester()
    sample_result = tester.run_popular_test_case(model)
    exe_time = time.time() - start_time
    self.__save_result(score, sample_result, exe_time, out_dir_path)
    self.__save_img(history, out_dir_path)


  def __gen_callbacks(self, early_stopping, slack, nb_epoch, out_dir_path):
    weight_save_path = os.path.join(out_dir_path, 'model_weights.h5')
    checkpointer = ModelCheckpoint(filepath=weight_save_path, verbose=1, save_best_only=True)
    callbacks = [LossHistory(), checkpointer]
    if early_stopping:
      callbacks.append(EarlyStopping(monitor='val_loss', patience=100, mode='min'))
    if slack:
      target_name = self.__fetch_target_name(out_dir_path)
      callbacks.append(SlackCallback(self.slack, nb_epoch, target_name))
    return callbacks

  def __fetch_output_directory(self, builder_path):
    return os.path.dirname(builder_path)

  def __fetch_target_name(self, directory_path):
      return os.path.basename(os.path.abspath(os.path.normpath(directory_path)))

  def __gen_model(self, builder_path):
    sys.path.append(os.path.dirname(builder_path))
    file_name = os.path.basename(builder_path)
    m = importlib.import_module(os.path.splitext(file_name)[0])
    builder = m.ModelBuilder()
    return builder.build()

  def __save_result(self, score, sample_result, exe_time, directory_path):
    with open(os.path.join(directory_path, 'result.txt'), 'w') as f:
      target_name = self.__fetch_target_name(directory_path)
      time_msg = "(exe_time = %d(s))" % exe_time
      result = "loss on test = %f\n\n" % score
      msg = "[RESULT] %s %s\n%s%s" % (target_name, time_msg, result, sample_result)
      f.write(msg)
      if self.params['slack']['result']:
        self.slack.post_message(msg)

  def __save_img(self, history, directory_path):
    target_name = self.__fetch_target_name(directory_path)
    X = np.arange(len(history.losses))
    plt.plot(X, history.losses, 'r', alpha=0.5, label='loss')
    plt.plot(X, history.val_losses, 'b', alpha=0.5, label='val_loss')
    plt.title(target_name)
    plt.legend()
    img_path = os.path.join(directory_path, 'loss_graph.png')
    plt.savefig(img_path)
    if self.params['slack']['result']:
      self.slack.post_image(img_path)

  def __save_model(self, model, directory_path):
    model_json = model.to_json()
    with open(os.path.join(directory_path, 'model_arrchitecture.json'), 'w') as f:
      f.write(model_json)

