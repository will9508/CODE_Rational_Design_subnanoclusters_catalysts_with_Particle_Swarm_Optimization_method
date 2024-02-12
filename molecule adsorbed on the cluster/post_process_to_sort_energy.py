import os

# Recursively traverse all folders and subfolders in the specified directory
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
                    #Get the folder name and its parent folder name
                    folder_names = foldername.split(os.path.sep)[-2:]
                    folder_names_str = " ".join(folder_names)
                    # Concatenate the value of the last line and the folder name into a string and add it to the list
                    data.append(f"{folder_names_str}: {last_line}")

    # Sort data
    data = sorted(data, key=lambda x: float(x.split(":")[-1]))

    # Write the sorted data to the energy_output.dat file
    with open("ENERGY_OUTPUT.dat", "w") as f_output:
        for item in data:
            f_output.write(f"{item}\n")

# Call the function to traverse all folders and subfolders in the current directory
traverse_folder(".")


def extract_values(file_path, top_n=1):
    values = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    sorted_lines = sorted(lines, key=lambda line: int(line.strip().split()[0].replace('gen', '')))

    for line in sorted_lines:
        data = line.strip().split()
        if len(data) >= 3:
            key = int(data[0].replace('gen', ''))
            value = float(data[2])

            if key not in values:
                values[key] = [value]
            else:
                values[key].append(value)

    header = "#gen  #the minimum value of the gen" if top_n == 1 else "#gen  #the minimum 5 values average of the gen"
    print(header)

    for key, value_list in values.items():
        value_list.sort()
        if top_n == 1:
            min_value = min(value_list)
            print(f"{key} {min_value}")
        else:
            average_min_values = sum(value_list[:5]) / min(len(value_list), 5)
            print(f"{key} {average_min_values}")


if __name__ == "__main__":
    file_path = "ENERGY_OUTPUT.dat"
    extract_values(file_path, top_n=1)
    extract_values(file_path, top_n=5)