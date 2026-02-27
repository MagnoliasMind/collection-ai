import numpy as np

points_A = np.random.randint(0, 100, size=(5, 2))
points_B = np.random.randint(0, 100, size=(8, 2))
points_A=points_A.reshape(5,1,2)
points_B=points_B.reshape(1,8,2)
diff = points_A - points_B
sqr = diff**2
distance_matrix = np.sqrt(np.sum(sqr,axis = 2))

min_dis_idx = np.unravel_index(np.argmin(distance_matrix,axis = 1))
print(distance_matrix[min_dis_idx])

bool_idx = (distance_matrix<20)
close_to = np.any(bool_idx,axis =0)
close = np.where(close_to)[0]