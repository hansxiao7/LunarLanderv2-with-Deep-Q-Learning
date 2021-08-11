import numpy as np

folder_location = 'replay_pool_size/'
file_name = 'r_list_100000_pool.txt'

r_list = np.loadtxt(folder_location+file_name)
average = []

for i in range(len(r_list)):
    if i < 99:
        average.append(np.mean(r_list[:i+1]))
    else:
        average.append(np.mean(r_list[i-99:i+1]))

np.savetxt(folder_location+'average_score_100000_pool.txt', average)