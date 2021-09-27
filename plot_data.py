#plot_data.py
from read_g2o import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from utility import *
from pose_graph import *

def draw_2d_vertex(state_vector, marker='o', color='b', size=10):
    x = round(float(state_vector[0]), 2)
    y = round(float(state_vector[1]), 2)
    plt.scatter(x, y, size, c=color, marker=marker)

def draw_3d_vertex(axes, state_vector, marker='o', color='b', size=10):
    x = round(float(state_vector[0]), 2)
    y = round(float(state_vector[1]), 2)
    z = round(float(state_vector[2]), 2)
    axes.scatter3D(x, y, z, zdir='z', s=size, c=color, marker=marker)

def draw_2d_transformation(T, marker='o', color='b', size=20):
    x,y,theta = trans2vec_2d(T)
    plt.scatter(x, y, size, c=color, marker=marker)

def draw_2d_connecting_edge(vec_1, vec_2, color='black', linestyle='solid', linewidth=1):
    x1,y1,theta1 = vec_1
    x2,y2,theta2 = vec_2

    x1 = round(float(x1), 3)
    y1 = round(float(y1), 3)
    x2 = round(float(x2), 3)
    y2 = round(float(y2), 3)

    plt.plot([x1, x2], [y1, y2], linestyle=linestyle, color=color, linewidth=linewidth)

def draw_3d_connecting_edge(axes, vec_1, vec_2, color='black', linestyle='solid', linewidth=1):
    x1,y1,z1,quat1 = vec_1
    x2,y2,z2,quat2 = vec_2

    x1 = round(float(x1), 3)
    y1 = round(float(y1), 3)
    z1 = round(float(z1), 3)
    x2 = round(float(x2), 3)
    y2 = round(float(y2), 3)
    z2 = round(float(z2), 3)

    axes.plot([x1, x2], [y1, y2], [z1, z2], zdir='z', linestyle=linestyle, color=color, linewidth=linewidth)

def draw_2d_all_states(vertex, edges={}, draw_start_end_node=0):
    for frame in vertex:
        draw_2d_vertex(vertex[frame])

    if draw_start_end_node != 0:
        draw_2d_vertex(vertex['0'], marker='*', color='r', size=100)
        last_node = list(vertex)[-1]
        draw_2d_vertex(vertex[last_node], marker='*', color='g', size=100)

    for frame in edges:
        for i in range(len(edges[frame])):
            frame_1 = edges[frame][i]["frame_1"]
            frame_2 = edges[frame][i]["frame_2"]

            draw_2d_connecting_edge(vertex[frame_1], vertex[frame_2], color='black', linestyle='solid', linewidth=1)

    plt.show()

def draw_3d_all_states(vertex, edges={}, draw_start_end_node=0):
    ax = plt.axes(projection='3d')

    for frame in vertex:
        draw_3d_vertex(ax, vertex[frame])

    if draw_start_end_node != 0:
        draw_3d_vertex(ax, vertex['0'], marker='*', color='r', size=100)
        last_node = list(vertex)[-1]
        draw_3d_vertex(ax, vertex[last_node], marker='*', color='g', size=100)

    for frame in edges:
        for i in range(len(edges[frame])):
            frame_1 = edges[frame][i]["frame_1"]
            frame_2 = edges[frame][i]["frame_2"]

            draw_3d_connecting_edge(ax, vertex[frame_1], vertex[frame_2], color='black', linestyle='solid', linewidth=1)

    plt.show()

if __name__ == "__main__":
    filename_1 = 'dataset/edges.txt'
    filename_2 = 'dataset/gt.txt'
    filename_3 = 'dataset/sphere_g2o_opti.g2o'

    # read the g2o file
    all_vertex, all_edges, anchor_frame, dim = parse_g2o_file(filename_3)

    if dim == '2D':
        draw_2d_all_states(all_vertex, all_edges)
    elif dim == '3D':
        draw_3d_all_states(all_vertex, all_edges)

