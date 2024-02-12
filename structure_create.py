#!/usr/bin/env python
# coding: utf-8

from ase.io import read
import numpy as np
from ase.io import read, write
from ase import Atoms

with open('structure.param', 'r') as f:
    lines = f.readlines()
    info_a = float(lines[0])
    info_b = float(lines[1])
    info_c = float(lines[2])
    info_x = float(lines[3])
    info_y = float(lines[4])
angle_x = np.pi * info_a
angle_y = np.pi * info_b
angle_z = np.pi * info_c

# Calculate the cluster rotation matrix
def cluster_rotation_matrix(angle_x, angle_y, angle_z, clusters):
    # Get the centroid of the Atoms object
    center_of_mass = clusters.get_center_of_mass()

    # Define the rotation angle in the x, y, z directions, in radians
    rotation_x = np.array([[1, 0, 0],
                           [0, np.cos(angle_x), -np.sin(angle_x)],
                           [0, np.sin(angle_x), np.cos(angle_x)]])

    rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                           [0, 1, 0],
                           [-np.sin(angle_y), 0, np.cos(angle_y)]])

    rotation_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                           [np.sin(angle_z), np.cos(angle_z), 0],
                           [0, 0, 1]])

    rotation_matrix = rotation_z @ rotation_y @ rotation_x

    # Rotate all atoms of the Atoms object around the center of mass and output absolute coordinates
    rotated_positions = np.dot(rotation_matrix,
                               (clusters.positions - center_of_mass).T).T + center_of_mass

    return rotated_positions

filename = 'cluster.poscar'  # Replaced with the actual Cluster POSCAR file
clusters = read(filename)

rotated_positions = cluster_rotation_matrix(angle_x, angle_y, angle_z, clusters)
print("rotated_positions\n",rotated_positions)

with open('structure.param', 'r') as f:
    lines = f.readlines()
    x_new = float(lines[-2])
    y_new = float(lines[-1])

print("x_new,y_new",x_new,y_new)

# Calculate the center of mass of the rotated_positions
center_of_mass_rotated = np.mean(rotated_positions, axis=0)

print("center_of_mass_rotated",center_of_mass_rotated)

# Calculate the translation vector to move the center of mass to (x_new, y_new)
translation_vector = np.array([x_new, y_new, 0]) - center_of_mass_rotated
print("translation_vector",translation_vector)


# Translate the rotated positions
translated_positions = rotated_positions + translation_vector

#Add a translation vector to the rotated coordinates

print(translated_positions)


# Find the smallest z-axis coordinate in the cluster after rotation and translation
min_z = np.min(translated_positions[:, 2])

# Calculate translation
translation_z = 2.5 - min_z

# Add a translation amount to the rotated and translated coordinates
translated_positions[:, 2] += translation_z

print(translated_positions)


# Read substrate.poscar file
substrate = read('substrate.poscar')

# Create a new Atoms object using the rotation, translation, and adjusted cluster coordinates and lattice constants of substrate.poscar
merged_positions = np.concatenate((substrate.positions, translated_positions), axis=0)
merged_symbols = substrate.get_chemical_symbols() + clusters.get_chemical_symbols()

merged_atoms = Atoms(
    positions=merged_positions,
    symbols=merged_symbols,
    cell=substrate.cell,
    pbc=True
)

# Write new Atoms objects to POSCAR files, using Cartesian format
write('POSCAR', merged_atoms, format='vasp', direct=False)
