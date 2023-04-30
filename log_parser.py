import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


input_filename = "energy.log"

outfile_name = 'asdf.tmp'

dict_filenames = "dict_filenames.log"
dict_stages = "dict_stages.log"

f = open(input_filename, 'r')
lines = f.readlines()




#From the main output file, split into sections

count = 0
names = []
delims = []
for line in lines:
    if line == "Starting...\n":
        print("Started")
    elif line[0:3] == '!!!':
        newName = outfile_name + str(count)
        names.append(newName)
        count += 1
        print(newName)
        print(line)
        delims.append(line)
    else:
        o = open(names[count - 1], 'a')
        o.write(line)
        o.close()


d = open(dict_filenames, "w")
for i in range(0, len(names)):
    name = names[i]
    d.write(name + '\n')
d.close()
d = open(dict_stages, "w")
for i in range(0, len(delims)):
    delim = delims[i]
    d.write(delim)
f.close()