#plot_data.py
from read_g2o import *
import matplotlib.pyplot as plt
from utility import *
from pose_graph import *

def draw_vertex(state_vector, marker='o', color='b', size=20):
    x = round(float(state_vector[0]), 2)
    y = round(float(state_vector[1]), 2)
    plt.scatter(x, y, size, c=color, marker=marker)

def draw_transformation(T, marker='o', color='b', size=20):
    x,y,theta = trans2vec_2d(T)
    plt.scatter(x, y, size, c=color, marker=marker)

def draw_connecting_edge(vec_1, vec_2, color='black', linewidth=2):
    x1,y1,theta1 = vec_1
    x2,y2,theta2 = vec_2

    x1 = round(float(x1), 3)
    y1 = round(float(y1), 3)
    x2 = round(float(x2), 3)
    y2 = round(float(y2), 3)

    plt.plot([x1, x2], [y1, y2], color=color)

def draw_all_states(vertex, edges):
    for frame in vertex:
        draw_vertex(vertex[frame])

    for frame in edges:
        for i in range(len(edges[frame])):
            frame_1 = edges[frame][i]["frame_1"]
            frame_2 = edges[frame][i]["frame_2"]

            draw_connecting_edge(vertex[frame_1], vertex[frame_2], color='black', linewidth=2)

    plt.show()

if __name__ == "__main__":
    filename_1 = 'dataset/edges.txt'
    filename_2 = 'dataset/gt.txt'

    # read the g2o file
    all_vertex, all_edges, anchor_frame = parse_g2o_file(filename_1)

    draw_all_states(vertex, edges)
