import argparse
import numpy as np
import pyquaternion

####################
## File Format
####################
# Vertex
### 2D Robot Pose
##### VERTEX_SE2 i x y theta
# Edges: 
##### EDGE_SE2 i j x y theta info(x, y, theta)

### 3D Robot Pose
##### VERTEX_SE3:QUAT i x y z qx qy qz qw

##### EDGE_SE3:QUAT i j x y z qx qy qz qw Omega11 Omega12 .. Omega16 Omega22 .. Omega26 Omega33 .. Omega36 Omega44 .. Omega46 Omega55 .. Omega56 Omega66
####################

anchor_frame_line = 'FIX'
edge_line_2d = "EDGE_SE2"
vertex_line_2d = "VERTEX_SE2"
landmark_line_2d = "VERTEX_XY"
edge_quat_3d = "EDGE_SE3:QUAT"
vertex_quat_3d = "VERTEX_SE3:QUAT"

def parse_2d_edge_line(line_data):
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

def parse_3d_edge_quat(line_data):
    ref_frame = line_data[1]
    frame = line_data[2]
    x = float(line_data[3])
    y = float(line_data[4])
    z = float(line_data[5])
    quat = pyquaternion.Quaternion(line_data[9], line_data[6], line_data[7], line_data[8])
    measurement = [x,y,z, quat]

    info_mat = np.zeros((6,6))
    itr = 0
    for i in range(0,6):
        for j in range(i,6):
            info_mat[i,j] = line_data[10+itr]
            info_mat[j,i] = line_data[10+itr]

            itr += 1

    return {"frame_1":ref_frame, "frame_2":frame, "measurement":measurement, "info_mat":info_mat}

def parse_2d_vertex_line(line_data):
    frame = line_data[1]
    x = float(line_data[2])
    y = float(line_data[3])
    theta = float(line_data[4])

    return {"frame_1":frame, "state_vector":[x,y,theta]}

def parse_3d_vertex_line(line_data):
    frame = line_data[1]
    x = float(line_data[2])
    y = float(line_data[3])
    z = float(line_data[4])
    quat = pyquaternion.Quaternion(line_data[8], line_data[5], line_data[6], line_data[7])
    return {"frame_1":frame, "state_vector":[x,y,z,quat]}

def parse_g2o_file(filename):
    file_reader = open(filename, 'r')
    file_lines = file_reader.readlines()

    vertex = {}
    edges = {}

    anchor_frame = None
    dim = 0

    for line in file_lines:
        coloums = line.split("\n")[0].split(' ')

        if coloums[0] == vertex_line_2d:
            vertex_dict = parse_2d_vertex_line(coloums)
            vertex[vertex_dict["frame_1"]] = vertex_dict["state_vector"]
            dim = '2D'

        elif coloums[0] == vertex_quat_3d:
            vertex_dict = parse_3d_vertex_line(coloums)
            vertex[vertex_dict["frame_1"]] = vertex_dict["state_vector"]
            dim = '3D'

        elif coloums[0] == edge_line_2d:
            edge_dict = parse_2d_edge_line(coloums)
            edges.setdefault(edge_dict["frame_1"], []).append(edge_dict)
            dim = '2D'

        elif coloums[0] == edge_quat_3d:
            edge_dict = parse_3d_edge_quat(coloums)
            edges.setdefault(edge_dict["frame_1"], []).append(edge_dict)
            dim = '3D'

        elif coloums[0] == anchor_frame_line:
            anchor_frame = coloums[1]

    return vertex, edges, anchor_frame, dim

if __name__ == '__main__':
    filename_1 = 'dataset/edges.txt'
    filename_2 = 'dataset/gt.txt'
    filename_3 = 'dataset/sphere.g2o'

    vertex, edges, anchor_frame, dim = parse_g2o_file(filename_3)

    print(dim)
    print(anchor_frame)
    print(edges['0'])

    print(edges['0'][0]["info_mat"])


