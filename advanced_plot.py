import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

input_names = "dict_filenames.log"
input_stages = "dict_stages.log"
FRAME_DELTA=1000
frame_output="frames.out"

stages = []
f = open(input_stages, 'r')
stages = f.readlines()
print(stages)
f.close()


f = open(input_names, 'r')
input_files = f.readlines()
f.close()
for i in range(0, len(input_files)):
    input_files[i] = input_files[i][0:len(input_files[i]) - 1]
    input_files[i] = input_files[i] + '.csv'
    print(input_files[i])

fig = plt.figure()

num_files = len(input_files)

time = []
temp = []
EPtot = []
delims = []
counts = []
count = 0
sizes = []
steps = []
for i in range(0, len(input_files)):
    data = pd.read_csv(input_files[i], ",")
    print("curr_input: ", input_files)
    length = len(data)
    data = data.drop([length - 1, length - 2])
    delims.append(count)
    for i in range(0, len(data)):
        row = data.loc[i]
        time.append(row['time'])
        temp.append(row['temp'])
        EPtot.append(row['EPtot'])
        counts.append(count)
        steps.append(row['step'])
        count += 1
        sizes.append(.1)


energy_ax = fig.add_subplot(211)
energy_ax.scatter(counts, EPtot, sizes)
temp_ax = fig.add_subplot(212)
temp_ax.scatter(counts, temp, sizes)
for i in range(0, len(delims)):
    delim = delims[i]
    energy_ax.plot([delim, delim], [-600, -10], 'red')
    energy_ax.text(delim, 0, stages[i][3:len(stages[i])])


#Now we want to find mins for each section

for i in range(1, len(steps)):
    if steps[i] < steps[i - 1]:
        print("Found a thing at ", i)

NUM_MINS = 10
#Find the top ten mins
mins = []
min_indices = []
min_sizes = [] #Just size of points
min_steps = []
sections = []

for i in range(0, NUM_MINS):
    currMin = 999
    minIndex = 0
    min_sizes.append(20)
    min_step = 0
    currSection = 0
    lastSection = 0
    for i in range(0, len(EPtot)):
        currEnergy = EPtot[i]
        if (i > 1):
            if steps[i] < steps[i - 1]:
                currSection += 1
        if currEnergy < currMin and i not in min_indices:
            currMin = currEnergy
            minIndex = i
            min_step = steps[i]
            lastSection = currSection
        
    mins.append(currMin)
    min_indices.append(minIndex)
    min_steps.append(min_step)
    sections.append(lastSection)

print("Min indices: ", min_indices)
print("Mins: ", mins)

energy_ax.scatter(min_indices, mins, min_sizes, c = 'red')

for i in range(0, len(mins)):
    step = min_steps[i]
    energy = mins[i]
    index = min_indices[i]
    #label = "#" + str(i) + ": s:" + str(step) + "\ne:" + str(energy) + "\ni:" + str(index)
    label = str(i)
    energy_ax.text(index, energy - 50, label) 
for i in range(0, len(min_steps)):
    print("Min #", i, ": step", min_steps[i], "section: ", sections[i])

#Save the filenames, and positions, of each min
outFrame = open(frame_output, "w")
for i in range(0, len(min_steps)):
    correctedStep = min_steps[i]//FRAME_DELTA
    section = sections[i]
    coordinate_file = 'last_' + str(section) + '.mdcrd'
    line = str(i) + ',' + coordinate_file + ',' + str(int(correctedStep)) + '\n'
    outFrame.write(line)
outFrame.close()
    

energy_ax.set_ylabel("Potential Energy")
temp_ax.set_ylabel("Temperature")
temp_ax.set_xlabel("Steps (Cumulative)")
plt.show()


