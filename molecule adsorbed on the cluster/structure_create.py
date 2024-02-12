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
#translation_vector = np.array([info_x, info_y, 0.0])

# ... (previous code)

# Read the last two lines of structure.param and set them as x and y
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

# Add a translation vector to the rotated coordinates

print(translated_positions)

# Find the smallest z-axis coordinate in the cluster after rotation and translation
#min_z = np.min(translated_positions[:, 2])

# Calculate translation
#translation_z = 4 - min_z

# Add a translation amount to the rotated and translated coordinates
#translated_positions[:, 2] += translation_z

#print(translated_positions)


# 读取 substrate.poscar 文件
substrate = read('substrate.poscar')

import numpy as np
from scipy.spatial import distance

# Calculate distances between each atom in translated_positions and substrate
distances = distance.cdist(translated_positions, substrate.positions)

# Define the target minimum distance range (between 1.0 and 1.5 angstroms)
target_min_distance = 1.6
target_max_distance = 2.1

while True:
    # Find the minimum distance
    min_distance = np.min(distances)

    if target_min_distance <= min_distance <= target_max_distance:
        break  # If the minimum distance is within the desired range, exit the loop

    # Move all atoms in the positive z-direction by 0.2 angstroms
    translated_positions[:, 2] += 0.2

    # Recalculate distances
    distances = distance.cdist(translated_positions, substrate.positions)

# At this point, the minimum distance is within the desired range (1.0 - 1.5 angstroms)



print(translated_positions)

# 创建新的 Atoms 对象，使用旋转、平移和调整后的簇坐标和 substrate.poscar 的晶格常数
merged_positions = np.concatenate((substrate.positions, translated_positions), axis=0)
merged_symbols = substrate.get_chemical_symbols() + clusters.get_chemical_symbols()

merged_atoms = Atoms(
    positions=merged_positions,
    symbols=merged_symbols,
    cell=substrate.cell,
    pbc=True
)

# 将新的 Atoms 对象写入 POSCAR 文件，使用 Cartesian 格式
write('POSCAR_unsort', merged_atoms, format='vasp', direct=False)

# 读取原始POSCAR文件
structure = read("POSCAR_unsort")

# 获取元素列表
elements = structure.get_chemical_symbols()

# 根据元素名称的首字母重新排序
sorted_structure = Atoms(cell=structure.cell)  # 复制原始结构的晶格参数

# 创建一个函数，用于从元素名称获取排序键
def sort_key(element_name):
    return element_name[0]

# 按照元素名称的首字母排序
sorted_indices = sorted(range(len(elements)), key=lambda i: sort_key(elements[i]))

# 使用排序后的索引重新排列原始结构
for idx in sorted_indices:
    sorted_structure.append(structure[idx])

# 将排序后的结构写入新的POSCAR文件
write("POSCAR", sorted_structure, format="vasp")

