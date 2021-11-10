# pose_graph_optimization_python
This is a python implementation of the pose graph optimization from scratch to understand the backend of Graph Slam. Moreover this can be used to implement a full graph slam solution in the future.

# What is Pose Graph Optimization
It is a graph based solution for non-linear optimization to update the poses while satisfying constraints. the contraints can come from loop closure or any other odometry sources such as gps. Overall, it is a way to actively fuse multiple sources of information to get the best possible pose.

# demo
python optimize_pose_graph.py dataset/intel.g2o --save_itr --output intel_optimized.g2o

This repo read odometry and constraints from .g2o file and outputs an optimized g2o file as well. This has been done to later validate the algorithm with the popular library 'g2o'.

G2O file format can be found here: https://github.com/RainerKuemmerle/g2o/wiki/File-Format-SLAM-2D

# intel dataset
![intel_opi](https://user-images.githubusercontent.com/20353960/141079035-9f608603-7cac-4fa2-b209-a68a4b141ac8.gif)

# References and Acknowledgements
1. Grisetti, G., Kummerle, R., Stachniss, C. and Burgard, W., 2010. A tutorial on graph-based SLAM. IEEE Intelligent Transportation Systems Magazine, 2(4), pp.31-43.
2. Carlone, L. and Censi, A., 2014. From angular manifolds to the integer lattice: Guaranteed orientation estimation with application to pose graph optimization. IEEE Transactions on Robotics, 30(2), pp.475-492.
3. Blanco, J.L., 2010. A tutorial on SE(3) transformation parameterizations and on-manifold optimization. University of Malaga, Tech. Rep, 3.
4. A Primer on the Differential Calculus of 3D Orientations, Michael Bloesch, https://arxiv.org/pdf/1606.05285.pdf.
5. Ein Rahmen für dünnbesetzte en.al. , A Framework for Sparse Non-Linear Least Squares Problems on Manifolds.

Thanks to Luca Carlone I was able to run and validate my efforts using datasets available here. ![Intel and parking dataset](https://lucacarlone.mit.edu/datasets/)

# To do
[] complete the 3d pose graph optimization
