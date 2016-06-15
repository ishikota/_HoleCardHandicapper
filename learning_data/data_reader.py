import csv
import random
import numpy as np

# HOW TO USE
# (X_train, y_train), (X_test, y_test) = data_reader.load_data("learning_data/data/100-data-at-1465816667.59.csv", 0.2)
#  >>> (X_train, y_train), (X_test, y_test) = data_reader.load_data("learning_data/data/100-data-at-1465816667.59.csv", test_ratio=0.3)
#  >>> X_train.shape
#  (92820, 52)
#  >>> y_train.shape
#  (92820,)
#  >>> X_test.shape
#  (39780, 52)
#  >>> y_test.shape
#  (39780,)
# memo : if hole ranks = [2,3] then X = [0,1,1,0,0,...] (len==52)


def load_data(file_path, test_ratio=0.0):
  data = []
  gen_one_hot = lambda h1, h2: [1 if i in [h1, h2] else 0 for i in range(1,53)]
  data_size = 0
  with open(file_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      data_size += 1
      y , hole1, hole2 = map(int, row[:3])
      X = gen_one_hot(hole1, hole2)
      if sum(X) != 2: raise "gen_hot_error on hole1=%d, hole2=%d" % (hole1, hole2)
      data += X
      data.append(y)

  data = np.array(data)
  data = data.reshape(data_size, 53)
  np.random.shuffle(data)
  learning_data_num = int(len(data) * (1 - test_ratio))
  learning_data = data[:learning_data_num]
  test_data = data[learning_data_num:]

  X_train = learning_data[:, :52]
  y_train = learning_data[:, 52]
  X_test = test_data[:, :52]
  y_test = test_data[:, 52]

  return (X_train, y_train), (X_test, y_test)

