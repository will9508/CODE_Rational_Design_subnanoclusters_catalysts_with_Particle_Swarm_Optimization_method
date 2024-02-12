import os

current_folder = os.getcwd()  # Get current folder path
def read_num_atoms_of_cluster():

    input_file_path = os.path.join(current_folder, "input.dat")
    with open(input_file_path) as input_file:
        for line in input_file:
            if line.startswith("num_atoms_cluster="):
                num_atoms_cluster= int(line.split("=")[1].strip())
                return num_atoms_cluster

    return None
num_atoms_of_cluster= read_num_atoms_of_cluster()
print(num_atoms_of_cluster)

from ase.io import read

# Read substrate.poscar file
atoms = read("substrate.poscar")

# Get the Cartesian coordinates of the last few atoms (cluster atoms)
last_atoms = atoms[-num_atoms_of_cluster:]

for i, atom in enumerate(last_atoms, start=1):
    print(f"Atom {i}: Symbol = {atom.symbol}, Cartesian Coordinates = {atom.position}")

# Get the minimum and maximum values of the x and y coordinates of the cluster atoms
min_x = min(atom.position[0] for atom in last_atoms)
min_y = min(atom.position[1] for atom in last_atoms)
max_x = max(atom.position[0] for atom in last_atoms)
max_y = max(atom.position[1] for atom in last_atoms)

# Define the surrounding range of cluster atoms
x_min_range = min_x - 0.5
x_max_range = max_x + 0.5
y_min_range = min_y - 0.5
y_max_range = max_y + 0.5

# Print range
print(f"x range: {x_min_range} to {x_max_range}")
print(f"y range: {y_min_range} to {y_max_range}")

output_file_path = os.path.join(current_folder, "xy_range.dat")
with open(output_file_path, 'w') as output_file:
    output_file.write(f" {x_min_range}  {x_max_range}\n")
    output_file.write(f" {y_min_range}  {y_max_range}\n")

print("Ranges written to xy_range.dat")
