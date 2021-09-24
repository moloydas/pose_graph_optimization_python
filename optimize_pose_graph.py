#optimize_pose_graphv2.py
from read_g2o import *
from utility import *
from pose_graph import *
from plot_data import *
import numpy as np
import math
import sys

if __name__ == "__main__":
    filename_1 = 'dataset/edges.txt'
    filename_2 = 'dataset/gt.txt'
    filename_3 = 'test_dataset.g2o'
    filename_4 = 'test_datasetv2.g2o'

    # read the g2o file
    all_vertex, all_edges, anchor_frame = parse_g2o_file(filename_4)

    # draw graph
    draw_all_states(all_vertex, all_edges)

    x = []
    for ref_frame in all_vertex:
        x.append(all_vertex[ref_frame])
    x = np.array(x).reshape(-1,1)
    n_states = x.shape[0]

    for itr in range(5):
        H = np.zeros((n_states, n_states))
        b = np.zeros((n_states,1))
        total_error = 0

        for frame in all_edges:
            for edge in all_edges[frame]:
                i_frame = edge["frame_1"]
                j_frame = edge["frame_2"]
                i = int(i_frame)

                x_i = x[3*i:3*i+3, 0]

                j = int(j_frame)
                t_i = vec2trans_2d(x_i)

                x_j = x[3*j:3*j+3, 0]
                t_j = vec2trans_2d(x_j)

                zij = edge["measurement"]
                info_mat = edge["info_mat"]

                #error cal
                eij = cal_eij(x_i, x_j, zij)

                # increment Total error
                total_error += eij.T @ info_mat @ eij

                # A B cal
                Aij, Bij = cal_jac_A_B(x_i, x_j, zij)

                H[3*i:3*i+3, 3*i:3*i+3] += Aij.T @ info_mat @ Aij
                H[3*i:3*i+3, 3*j:3*j+3] += Aij.T @ info_mat @ Bij
                H[3*j:3*j+3, 3*i:3*i+3] += Bij.T @ info_mat @ Aij
                H[3*j:3*j+3, 3*j:3*j+3] += Bij.T @ info_mat @ Bij

                b[3*i:3*i+3, 0] += np.squeeze(Aij.T @ info_mat @ eij)
                b[3*j:3*j+3, 0] += np.squeeze(Bij.T @ info_mat @ eij)

        H[:3,:3] += np.eye(3)

        print(f'itr: {itr}')
        print(f'total error: {total_error}')

        # optimize
        delta_x = np.linalg.inv(H) @ -b
        x += delta_x

    new_vertex = create_vertex_from_state_vector(x.reshape(-1, 3))

    draw_all_states(new_vertex, all_edges)
