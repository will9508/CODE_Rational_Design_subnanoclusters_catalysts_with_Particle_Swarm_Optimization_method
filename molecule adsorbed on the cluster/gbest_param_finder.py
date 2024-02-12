import os
import shutil

parent_directory = "./"  # 
min_value = float("inf")
min_value_file = None

# Iterate through all files in the parent directory and its subdirectories
for root, dirs, files in os.walk(parent_directory):
    for filename in files:
        if filename.endswith("structure.param"):
            file_path = os.path.join(root, filename)
            # Read the value of the last line of the file and update the file with minimum and minimum values
            with open(file_path, "r") as f:
                last_line = f.readlines()[-1].strip()
                value = float(last_line.split()[-1])
                if value < min_value:
                    min_value = value
                    min_value_file = file_path

# Copy the minimum value file to the current directory and rename it to gbest.param
if min_value_file is not None:
    shutil.copy(min_value_file, "./gbest.param")

