import numpy as np
data_matrix = np.arange(100).reshape((10,10))
print(data_matrix[4:8,4:8])

bool_idx = (data_matrix>75)
data_matrix[bool_idx] = 0
print(data_matrix)
data_matrix.dtype = float
print(data_matrix.dtype)
#b = np.full((10,10),0.8)
#data_matrix = data_matrix*b
data_matrix *= 0.8
print(data_matrix)
idx = np.unravel_index(np.argmax(data_matrix),data_matrix.shape)
print(data_matrix[idx])
