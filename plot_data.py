#plot_data.py
from read_g2o import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from utility import *
from pose_graph import *

def draw_2d_vertex(state_vector, size, **kwargs):
    x = np.around(state_vector[:,0].astype(np.float32), 2)
    y = np.around(state_vector[:,1].astype(np.float32), 2)
    plt.scatter(x, y, size, **kwargs)

def draw_3d_vertex(axes, state_vector, size=10, **kwargs):
    x = np.around(state_vector[:,0].astype(np.float32), 2)
    y = np.around(state_vector[:,1].astype(np.float32), 2)
    z = np.around(state_vector[:,2].astype(np.float32), 2)
    axes.scatter3D(x, y, z, zdir='z', s=size, **kwargs)

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

def draw_2d_all_states(vertex, edges={}, draw_start_end_node=0, plot_immediate=1, **kwargs):
    vertex_list = []
    for frame in vertex:
        vertex_list.append(vertex[frame])

    draw_2d_vertex(np.array(vertex_list), 10, **kwargs)

    if draw_start_end_node != 0:
        draw_2d_vertex(np.array([vertex['0']]), size=100, marker='*', color='r')
        last_node = list(vertex)[-1]
        draw_2d_vertex(np.array([vertex[last_node]]), size=100, marker='*', color='g')

    for frame in edges:
        for i in range(len(edges[frame])):
            frame_1 = edges[frame][i]["frame_1"]
            frame_2 = edges[frame][i]["frame_2"]

            draw_2d_connecting_edge(vertex[frame_1], vertex[frame_2], color='black', linestyle='solid', linewidth=1)

    plt.legend()
    plt.xlabel('X(m)')
    plt.ylabel('Y(m)')
    if plot_immediate == 1:
        plt.show()

def draw_3d_all_states(vertex, edges={}, draw_start_end_node=0, plot_immediate=1, **kwargs):
    ax = plt.axes(projection='3d')

    vertex_list = []
    for frame in vertex:
        vertex_list.append(vertex[frame])

    draw_3d_vertex(ax, np.array(vertex_list), 10, **kwargs)

    if draw_start_end_node != 0:
        draw_3d_vertex(ax, np.array([vertex['0']]), size=100, marker='*', color='r')
        last_node = list(vertex)[-1]
        draw_3d_vertex(ax, np.array([vertex[last_node]]), size=100, marker='*', color='g')

    for frame in edges:
        for i in range(len(edges[frame])):
            frame_1 = edges[frame][i]["frame_1"]
            frame_2 = edges[frame][i]["frame_2"]

            draw_3d_connecting_edge(ax, vertex[frame_1], vertex[frame_2], color='black', linestyle='solid', linewidth=1)

    plt.legend()
    plt.xlabel('X(m)')
    plt.ylabel('Y(m)')
    if plot_immediate == 1:
        plt.show()

if __name__ == "__main__":
    filename_1 = 'dataset/complete_edges_optimized.g2o'
    filename_2 = 'dataset/gt.txt'
    filename_3 = 'dataset/sphere_g2o_opti.g2o'
    filename_4 = 'dataset/complete_edges_g2o_optimized.g2o'

    # read the file
    all_vertex, all_edges, anchor_frame, dim = parse_g2o_file(filename_4)
    draw_2d_all_states(all_vertex, all_edges, draw_start_end_node=1, plot_immediate=0, color='blue', label='G2O')

    # plot additional data multiple plots
    all_vertex, all_edges, anchor_frame, dim = parse_g2o_file(filename_1)
    draw_2d_all_states(all_vertex, all_edges, draw_start_end_node=1, plot_immediate=0, color='red', label='this_code')

    plt.title('G2O vs this_code')
    plt.show()

    #plot 3d plot
    all_vertex, all_edges, anchor_frame, dim = parse_g2o_file(filename_3)
    draw_3d_all_states(all_vertex, all_edges, draw_start_end_node=1, plot_immediate=0, label='g2o')
    plt.title('G2O Optimized sphere')
    plt.show()
