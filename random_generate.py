#!/usr/bin/env python
# coding: utf-8

import random

def random_list():
    # Read x and y range values from xy_range.dat
    with open('xy_range.dat', 'r') as range_file:
        lines = range_file.readlines()
        if len(lines) >= 2:
            x_range = [float(value) for value in lines[0].split()]
            y_range = [float(value) for value in lines[1].split()]
        else:
            raise ValueError("The xy_range.dat file should contain at least two lines with x and y ranges.")

    # Generate random_x and random_y values within their respective ranges
    random_x = random.uniform(x_range[0], x_range[1])
    random_y = random.uniform(y_range[0], y_range[1])

    # Generate the other random values as before
    random_a = random.uniform(-1, 1)
    random_b = random.uniform(-0.5, 0.5)
    random_c = random.uniform(-1, 1)

    # Write all random values to the "structure.param" file
    with open('structure.param', 'w') as f:
        f.write(f'{random_a}\n')
        f.write(f'{random_b}\n')
        f.write(f'{random_c}\n')
        f.write(f'{random_x}\n')
        f.write(f'{random_y}\n')

    # Print the random values
    print('random for rotation\n', random_a, random_b, random_c, '\nrandom for displacement\n', random_x, random_y)

# Call the random_list function to generate and write the random numbers
random_list()

