import argparse
import numpy as np

####################
## File Format
####################
# Vertex
### 2D Robot Pose
##### VERTEX_SE2 i x y theta
# Edges: 
##### EDGE_SE2 i j x y theta info(x, y, theta)
####################

anchor_frame_line = 'FIX'
edge_line = "EDGE_SE2"
vertex_line = "VERTEX_SE2"
landmark_line = "VERTEX_XY"

def parse_edge_line(line_data):
    ref_frame = line_data[1]
    frame = line_data[2]
    x = float(line_data[3])
    y = float(line_data[4])
    theta = float(line_data[5])
    measurement = [x,y,theta]

    infor_mat = np.zeros((3,3))
    infor_mat[0,0] = float(line_data[6])
    infor_mat[0,1] = float(line_data[7])
    infor_mat[0,2] = float(line_data[8])
    infor_mat[1,1] = float(line_data[9])
    infor_mat[1,2] = float(line_data[10])
    infor_mat[2,2] = float(line_data[11])

    return {"frame_1":ref_frame, "frame_2":frame, "measurement":measurement, "info_mat":infor_mat}

def parse_vertex_line(line_data):
    frame = line_data[1]
    x = float(line_data[2])
    y = float(line_data[3])
    theta = float(line_data[4])

    return {"frame_1":frame, "state_vector":[x,y,theta]}

def parse_g2o_file(filename):
    file_reader = open(filename, 'r')
    file_lines = file_reader.readlines()

    vertex = {}
    edges = {}

    anchor_frame = None

    for line in file_lines:
        coloums = line.split("\n")[0].split(' ')

        if coloums[0] == vertex_line:
            vertex_dict = parse_vertex_line(coloums)
            vertex[vertex_dict["frame_1"]] = vertex_dict["state_vector"]

        elif coloums[0] == edge_line:
            edge_dict = parse_edge_line(coloums)

            edges.setdefault(edge_dict["frame_1"], []).append(edge_dict)

        elif coloums[0] == anchor_frame_line:
            anchor_frame = coloums[1]

    return vertex, edges, anchor_frame

if __name__ == '__main__':
    filename_1 = 'dataset/edges.txt'
    filename_2 = 'dataset/gt.txt'

    vertex, edges, anchor_frame = parse_g2o_file(filename_2)

    print(anchor_frame)
    print(edges[0])


