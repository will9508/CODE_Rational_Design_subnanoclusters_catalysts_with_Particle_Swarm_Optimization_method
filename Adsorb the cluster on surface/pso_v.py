import random


w = 0.1
c1 = 0.16
c2 = 0.84

# Generate random numbers r1 and r2
r1 = random.uniform(0, 1)
r2 = random.uniform(0, 1)

#Read data from velocity.dat, structure.dat and gbest.dat files
velocity_lines = open('velocity_backup.dat', 'r').readlines()[:5]
structure_lines = open('structure_backup.param', 'r').readlines()[:5]
gbest_lines = open('gbest_backup.param', 'r').readlines()[:5]
pbest_lines = open('pbest_backup.param', 'r').readlines()[:5]

# Calculate each line and store the results into the new_lines list
new_lines = []
for i in range(len(velocity_lines)):
    v_elements = velocity_lines[i].strip().split()
    s_elements = structure_lines[i].strip().split()
    g_elements = gbest_lines[i].strip().split()
    p_elements = pbest_lines[i].strip().split()
    pbest = float(p_elements[0])
    structure = float(s_elements[0])
    gbest = float(g_elements[0])
    velocity=float(v_elements[0])
    p = pbest - structure
    g = gbest - structure
    new_v_elements = []
    for j in range(len(v_elements)):
        v = w * float(v_elements[j])
        new_v = v + c1 * r1 * p + c2 * r2 * g
        new_v_elements.append(str(new_v))
    new_line = ' '.join(new_v_elements) + '\n'
    new_lines.append(new_line)

# Write the results to the velocity_new.dat file
with open('velocity.dat', 'w') as f:
    f.writelines(new_lines)

# Output the values of r1, r2, c1 and c2
print("r1 =", r1)
print("r2 =", r2)
print("c1 =", c1)
print("c2 =", c2)
