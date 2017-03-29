import numpy as np
from api import *

w_h = np.load('w_h.npy')
w_h2 = np.load('w_h2.npy')
w_o = np.load('w_o.npy')
print (w_h)
print (w_h2)
print (w_o)

data = seqData()
train_data = data[0:9000,:]
test_data = data[9000:,:]

