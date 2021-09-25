#pose_graph.py
from read_g2o import *
from utility import *

def cal_jac_A_B(x_i, x_j, z_ij):
    R_ij = angle2mat_2d(z_ij[2])
    R_i = angle2mat_2d(x_i[2])

    d_R_i = np.array([  [-math.sin(x_i[2]), -math.cos(x_i[2])],
                        [math.cos(x_i[2]), -math.sin(x_i[2])]   ])
    del_t = (x_j[:2] - x_i[:2]).reshape(2,1)

    A = np.zeros((3,3))
    A[:2,:2] = -R_ij.T @ R_i.T
    A[:2,2] = np.squeeze(R_ij.T @ d_R_i.T @ del_t)
    A[2,2] = -1

    B = np.eye(3)
    B[:2,:2] = R_ij.T @ R_i.T

    return A,B

def cal_eij(x_i, x_j, z_ij):
    R_ij = angle2mat_2d(z_ij[2])
    R_i = angle2mat_2d(x_i[2])

    del_t = (x_j[:2] - x_i[:2]).reshape(2,1)
    del_t_ij = np.array(z_ij)[:2].reshape(2,1)

    eij_t = R_ij.T @ ((R_i.T @ del_t) - del_t_ij)
    eij_theta = x_j[2] - x_i[2] - z_ij[2]
    eij_theta = limit_angles(eij_theta)

    eij = np.vstack((eij_t, eij_theta))
    return eij


