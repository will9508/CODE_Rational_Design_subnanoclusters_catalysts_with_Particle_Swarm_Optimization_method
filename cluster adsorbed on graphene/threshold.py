# -*- coding: utf-8 -*-

import os

def read_threshold_value():
    current_folder = os.getcwd()  # Get current folder path
    parent_folder = os.path.dirname(current_folder)  # Get parent folder path

    input_file_path = os.path.join(parent_folder, "input.dat")
    with open(input_file_path) as input_file:
        for line in input_file:
            if line.startswith("threshold="):
                threshold_value = int(line.split("=")[1].strip())
                return threshold_value

    return None

def traverse_folder(root_folder):
    data = []
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == "structure.param":
                file_path = os.path.join(foldername, filename)
                # Read last line of file
                with open(file_path) as f:
                    lines = f.readlines()
                    last_line = lines[-1].strip()
                    # Concatenate the value of the last line and the folder name into a string and add it to the list
                    data.append(f"{last_line}")

    # Sort data
    data = sorted(data, key=lambda x: float(x.split(":")[-1]))

    # Write the sorted data to the energy_output.dat file
    with open("gen_energy_output.dat", "w") as f_output:
        for item in data:
            f_output.write(f"{item}\n")

    threshold = read_threshold_value() - 1
    with open("threshold.dat", "w") as t_output:
        t_output.write(data[threshold])

current_folder = os.getcwd()
traverse_folder(current_folder)
# print(read_threshold_value() - 1)