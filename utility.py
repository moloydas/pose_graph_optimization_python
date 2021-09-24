#utility.py
import math
import numpy as np

def vec2trans_2d(vec):
    x = vec[0]
    y = vec[1]
    theta = float(vec[2])

    T = np.zeros((3,3))
    T[0,2] = round(float(x), 3)
    T[1,2] = round(float(y), 3)
    T[2,2] = 1

    T[0,0] = math.cos(theta)
    T[0,1] = -math.sin(theta)
    T[1,0] = math.sin(theta)
    T[1,1] = math.cos(theta)

    return T

def trans2vec_2d(T, return_type=None):
    x = T[0,2]
    y = T[1,2]

    theta = math.atan2(T[1,0], T[0,0])

    if return_type == 'numpy':
        return np.array([x,y,theta])
    elif return_type == 'list':
        return [x,y,theta]
    else:
        return x,y,theta

def angle2mat_2d(theta):
    R = np.array([  [math.cos(theta), -math.sin(theta)],
                    [math.sin(theta), math.cos(theta)] ])

    return R

# keep angles between -pi to pi
def limit_angles(theta):
    if theta > np.pi:
        delta = theta - np.pi
        return -delta
    elif theta < -np.pi:
        delta = abs(theta) - np.pi
        return np.pi - delta
    else:
        return theta

# this function expects vertex and edges
# vertex format:{"frame_1":frame, "measurement":[x,y,theta]} 
# edges format :{"frame_1":ref_frame, "frame_2":frame, "measurement":[del_x, del_y, del_theta], "info_mat":np.array: 3x3 }
def write_g2o_file(filename, vertex, edges):
    g2o_file = open(filename, 'w+')

    for frame in vertex:
        line = "VERTEX_SE2 " + str(frame) + " " + str(vertex[frame][0]) + " " + str(vertex[frame][1]) + " " + str(vertex[frame][2]) + '\n'
        g2o_file.write(line)

    for frame in edges:
        frame_1 = frame
        frame_2 = edges[frame]["frame_2"]
        infor_mat = edges[frame]["info_mat"]

        info_mat_txt = str(infor_mat[0,0])
        info_mat_txt += " " + str(infor_mat[0,1])       
        info_mat_txt += " " + str(infor_mat[0,2])
        info_mat_txt += " " + str(infor_mat[1,1])
        info_mat_txt += " " + str(infor_mat[1,2])
        info_mat_txt += " " + str(infor_mat[2,2])

        line = "EDGE_SE2 " + str(frame_1) + " " + str(frame_2) + " " + str(vertex[frame][0]) + " " + str(vertex[frame][1]) + " " + str(vertex[frame][2]) + " " + info_mat_txt + '\n'

        g2o_file.write(line)

    g2o_file.close()
