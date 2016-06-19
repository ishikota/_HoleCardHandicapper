import numpy as np

def load_data(file_path, test_ratio):
  num_training, num_testing, sigma, seed = 400, 100, 0.3, 0
  def sin(x):
      return np.sin(x)*3+1
  N = num_training + num_testing
  tau=4*np.pi
  np.random.seed(seed)
  X = np.random.random((N,1))*tau
  Y = sin(X)+np.random.normal(0,sigma,(N,1))
  I = np.arange(N)
  np.random.shuffle(I)
  training, testing = I[:num_training], I[num_training:]
  return (X[training], Y[training]), (X[testing], Y[testing])

