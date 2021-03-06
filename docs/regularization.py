#!/usr/bin/env python
# coding: utf-8



from saenopy import FiniteBodyForces
    
# initialize the object
M = FiniteBodyForces()


from saenopy.materials import SemiAffineFiberMaterial

# provide a material model
material = SemiAffineFiberMaterial(1645, 0.0008, 0.0075, 0.033)
M.setMaterialModel(material)


import numpy as np

# define the coordinates of the nodes of the mesh
# the array has to have the shape N_v x 3
R = np.array([[0., 0., 0.],  # 0
              [0., 1., 0.],  # 1
              [1., 1., 0.],  # 2
              [1., 0., 0.],  # 3
              [0., 0., 1.],  # 4
              [1., 0., 1.],  # 5
              [1., 1., 1.],  # 6
              [0., 1., 1.]]) # 7

# define the tetrahedra of the mesh
# the array has to have the shape N_t x 4
# every entry is an index referencing a verces in R (indices start with 0)
T = np.array([[0, 1, 7, 2],
              [0, 2, 5, 3],
              [0, 4, 5, 7],
              [2, 5, 6, 7],
              [0, 7, 5, 2]])


# provide the node data
M.setNodes(R)
# and the tetrahedron data
M.setTetrahedra(T)


# the displacements of the nodes which shall be fitted
# during the solving
U = np.array([[0   , 0, 0],  # 0
              [0   , 0, 0],  # 1
              [0.01, 0, 0],  # 2
              [0.01, 0, 0],  # 3
              [0   , 0, 0],  # 4
              [0.01, 0, 0],  # 5
              [0.01, 0, 0],  # 6
              [0   , 0, 0]]) # 7

# hand the displacements over to the class instance
M.setTargetDisplacements(U)


# relax the mesh and move the "varible" nodes
M.regularize(stepper=0.1, alpha=0.001)


results = M.computeForceMoments(rmax=100e-6)

# store the forces of the nodes
M.storeF("F.dat")
# store the positions and the displacements
M.storeRAndU("R.dat", "U.dat")
# store the center of each tetrahedron and a combined list with energies and volumina of the tetrahedrons
M.storeEandV("RR.dat", "EV.dat")

M.U

M.viewMesh(50, 1)

