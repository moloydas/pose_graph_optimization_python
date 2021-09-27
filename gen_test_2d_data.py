#gen_test_data.py
import numpy as np
import matplotlib.pyplot as plt
from utility import *
import math

# generate a small test dataset to test the code
# dataset:
# 0: (0,0,0)
# 1: (1,0, 90)
# 2: (1, 1, 180)
# 3: (0, 1, 270)
# 4: (0, 0, 0)
# 4: 0

def cal_pose_odom(x_i, delta_x):
    R = np.array([  [math.cos(x_i[2]), -math.sin(x_i[2]), 0], 
                    [math.sin(x_i[2]), math.cos(x_i[2]), 0],
                    [0,0,1]     ])
    
    x_j = np.array(x_i).reshape(3,1) + R @ np.array(delta_x).reshape(3,1)
    return x_j

if __name__ == '__main__':
    gt = {  '0': {"state_vector": [0,0,0], "connected_frame":['world', '1']},
            '1': {"state_vector": [1,0,np.pi/2], "connected_frame":['0', '2']},
            '2': {"state_vector": [1,1,np.pi], "connected_frame":['1', '3']},
            '3': {"state_vector": [0,1,-np.pi/2], "connected_frame":['2', '4']},
            '4': {"state_vector": [0,0,0], "connected_frame":['3', '0']}    }

    p_noise = 0.05
    theta_noise = 0.05

    anchor_frame = None

    odometry = []
    edges = []
    i = 0
    for frame in gt:
        if gt[frame]["connected_frame"][0] == 'world':
            anchor_frame = frame
            odometry.append(np.array(gt[frame]["state_vector"]).reshape(3,1))
            continue

        o_t_j = vec2trans_2d(gt[frame]["state_vector"])
        o_t_i = vec2trans_2d(odometry[i])
        i_t_j = np.linalg.inv(o_t_i) @ o_t_j
        del_x, del_y, del_theta = trans2vec_2d(i_t_j)

        del_x_noisy = np.random.normal(del_x, p_noise)
        del_y_noisy = np.random.normal(del_y, p_noise)
        del_theta_noisy = np.random.normal(del_theta, theta_noise)

        edges.append([del_x_noisy, del_y_noisy, del_theta_noisy])

        x_j = cal_pose_odom(odometry[i], [del_x_noisy, del_y_noisy, del_theta_noisy])        
        odometry.append(x_j)        
        i += 1

    test_data_file = open('test_datasetv2.g2o', 'w+')

    for i in range(5):
        line = "VERTEX_SE2 " + str(i) + " " + str(odometry[i][0,0]) + " " + str(odometry[i][1,0]) + " " + str(odometry[i][2,0]) + '\n'
        test_data_file.write(line)

    info_mat = "{info:.2f} 0.0 0.0 {info:.2f} 0.0 {info:.2f}".format(info=1/p_noise)
    for i,pose in enumerate(edges):
        line = "EDGE_SE2 "+str(i)+" "+str(i+1)+" "+str(pose[0])+" "+str(pose[1])+" "+str(pose[2])+" "+info_mat+'\n'
        test_data_file.write(line)

    # test_data_file.write("FIX 0\n")

    measurement_noise = 0.01
    measurement = np.random.normal(np.zeros((3,1)), measurement_noise, size=(3,1))
    info_mat = "{info:.2f} 0.0 0.0 {info:.2f} 0.0 {info:.2f}".format(info=1/measurement_noise)

    line = "EDGE_SE2 "+str(4)+" "+str(0)+" "+str(measurement[0,0])+" "+str(measurement[1,0])+" "+str(measurement[2,0])+" "+info_mat+'\n'
    test_data_file.write(line)

    measurement_2 = np.array(gt['2']["state_vector"]).reshape(3,1)
    measurement_noise_vec = np.random.normal(np.zeros((3,1)), measurement_noise, size=(3,1))
    measurement_2_noisy = measurement_2 + measurement_noise_vec
    line = "EDGE_SE2 "+str(4)+" "+str(2)+" "+str(measurement_2_noisy[0,0])+" "+str(measurement_2_noisy[1,0])+" "+str(measurement_2_noisy[2,0])+" "+info_mat+'\n'
    test_data_file.write(line)

    #plot the trajectory
    for frame in gt:
        ref_pose = gt[frame]["state_vector"]
        next_frame = gt[frame]["connected_frame"][1]
        next_pose = gt[next_frame]["state_vector"]
        plt.plot([ref_pose[0], next_pose[0]], [ref_pose[1], next_pose[1]], 'r-o', label='gt')

    for i,ref_pose in enumerate(odometry):
        if i+1 >= len(odometry):
            break
        next_pose = odometry[i+1]
        plt.plot([ref_pose[0], next_pose[0]], [ref_pose[1], next_pose[1]], 'b-o', label='gt')

    plt.show()

