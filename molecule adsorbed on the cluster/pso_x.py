# Read the data in the first five lines of velocity.dat and structure_backup.param files

def xy_range():
    # Read x and y range values from xy_range.dat
    with open('xy_range.dat', 'r') as range_file:
        lines = range_file.readlines()
        if len(lines) >= 2:
            x_range = [float(value) for value in lines[0].split()]
            y_range = [float(value) for value in lines[1].split()]

xy_range()

with open('velocity.dat', 'r') as f:
    velocity_lines = f.readlines()[:5]

with open('structure_backup.param', 'r') as f:
    structure_lines = f.readlines()[:5]

#Add each row in velocity_lines and structure_lines and store the result in new_lines
limits = [(-1, 1), (-0.5, 0.5), (-1, 1), (x_range[0], x_range[1]), (y_range[0], y_range[1])]
new_lines = []
for i in range(5):
    velocity_elements = velocity_lines[i].strip().split()
    structure_elements = structure_lines[i].strip().split()
    new_elements = []
    for j in range(len(velocity_elements)):
        new_value = float(velocity_elements[j]) + float(structure_elements[j])
        limit = limits[i]
        new_value = min(max(new_value, limit[0]), limit[1])
        new_elements.append(str(new_value))
    new_line = ' '.join(new_elements) + '\n'
    new_lines.append(new_line)

#Write new_lines into the structure.param file
with open('structure.param', 'w') as f:
    f.writelines(new_lines)

