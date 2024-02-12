import os

# Get the value of the last line of the structure.dat file
with open('structure.param', 'r') as f:
    structure_dat_value = f.readlines()[-1].strip()

# Get the value of the last line of the pbest_backup.param file
with open('pbest_backup.param', 'r') as f:
    pbest_backup_param_value = f.readlines()[-1].strip()

# Convert string type numeric value to floating point number for comparison
if float(structure_dat_value) < float(pbest_backup_param_value):
    # If so, set the structure.dat file to the pbest.param file
    os.system('cp structure.param pbest.param')
else:
    # Otherwise set the pbest_backup.param file to the pbest.param file
    os.system('cp pbest_backup.param pbest.param')

