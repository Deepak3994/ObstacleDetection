# ObstacleDetection
A Stationary and Moving Obstacle Segmentation System


An approach for modeling the 3D dynamic driving scene using a set of variable-size planes and arrays of voxels. 3D-LIDAR and GPS-aided
Inertial Navigation System (INS) data are used as inputs. The set of variablesize planes are used to estimate and model non-planar grounds, such as undulated
roads and curved uphill - downhill ground surfaces. The voxel pattern representation is used to efficiently model obstacles, which are further segmented into: static obstacles and moving obstacles
Watch the result in the video below.

https://youtu.be/o5oqtT6bXa0

![picture1](https://user-images.githubusercontent.com/5465785/43979846-f716f6b8-9ce3-11e8-8a52-9daa12f71aa1.png)

The algorithm is described in:

A. Asvadi, C. Premebida, P. Peixoto, and U. Nunes, “3D Lidar-based Static and Moving Obstacle Detection in Driving Environments: an approach based on voxels and multi-region ground planes,” Robotics and Autonomous Systems (RAS), vol. 83, pp. 299–311, September 2016. DOI: 10.1016/j.robot.2016.06.007 

A. Asvadi, P. Peixoto, and U. Nunes, “Two-Stage Static/Dynamic Environment Modeling Using Voxel Representation,” Robot 2015: Second Iberian Robotics Conference. Springer International Publishing, vol. 1, pp. 465-476, 2016. (Book Chapter) DOI: 10.1007/978-3-319-27146-0_36

Use smop to convert from matlab to python.
