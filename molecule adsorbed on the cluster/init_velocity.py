#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random

def random_list():
# Generate 5 random numbers
    random_v1 = random.uniform(-0.3, 0.3)
    random_v2 = random.uniform(-0.3, 0.3)
    random_v3 = random.uniform(-0.3, 0.3)
    random_v4 = random.uniform(-0.3, 0.3)
    random_v5 = random.uniform(-0.3, 0.3)

# Write random numbers to file
    with open('velocity.dat', 'w') as f:
        f.write(f'{random_v1}\n')
        f.write(f'{random_v2}\n')
        f.write(f'{random_v3}\n')
        f.write(f'{random_v4}\n')
        f.write(f'{random_v5}\n')

# Print random numbers
    print('velocity\n',random_v1, random_v2, random_v3, random_v4, random_v5)


# In[ ]:


#If you would like to have random list, pls run this code, or prepare info.txt.by yourself
random_list()

