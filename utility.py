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

