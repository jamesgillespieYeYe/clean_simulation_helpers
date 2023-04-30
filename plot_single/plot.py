import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


ZOOM_ON_MIN = True
ZOOM_NUM = 20
marker_size=.1
input_file = "final.csv"
title = "default title"
SHOULD_PLOT=True
for arg in sys.argv:
    split = arg.split(':')
    if split[0] == '-i':
        input_file = split[1]
    elif split[0] == '-t':
        title = split[1]
    elif split[0] == '-np':
        SHOULD_PLOT=False
print("Input file:", input_file, ",", "title: ", title)

data = pd.read_csv(input_file, ",")
length = len(data)
#Get rid of last two entries as they are from summary at end of file
data = data.drop([length - 1, length - 2])


NUM_MINS = 10
minEnergy = 999
minStep = 0
minTime = 0
minIndex = 0
for i in range(0, len(data)):
    row = data.loc[i]
    energy = row['EPtot']
    step = row['step']
    time = row['time']
    if energy < minEnergy:
        minEnergy = energy
        minStep = step
        minTime = time
        minIndex = i

mins = []
min_indices = []
min_sizes = []
min_steps = []
min_temps = []
for j in range(0, NUM_MINS):
    currMin = 999
    min_index = 0
    min_sizes.append(20)
    min_step = 0
    print(j)
    for i in range(0, len(data)):
        currEnergy = data.loc[i]['EPtot']
        if currEnergy < currMin and i not in min_indices:
            currMin = currEnergy
            min_index = i
            min_step = data.loc[i]['step']
    mins.append(currMin)
    min_indices.append(min_index)
    min_steps.append(min_step)

print("Min indices: ", min_indices)
print("Mins: ", mins)  
    
print("Minimum energy occurs at time:", minTime, "step:", minStep, "energy: ", minEnergy)

if SHOULD_PLOT == True:
    sizes = []
    colors = []
    for i in range(0, len(data)):
        if (i == minIndex or i in min_indices):
            sizes.append(50)
            colors.append('red')
        else:
            sizes.append(marker_size)
            colors.append('blue')
        




    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.scatter(data['time'], data['EPtot'], sizes,c=colors)
    ax1.set_ylabel("EPtot")

    ax2 = fig.add_subplot(212)
    ax2.scatter(data['time'], data['temp'], sizes)
    ax2.set_ylabel("Temperature (K)")
    ax2.set_xlabel("Time")


    # secondFig = plt.figure()
    # secondAx1 = secondFig.add_subplot(211)
    # secondAx2 = secondFig.add_subplot(212)
    # bound = 50
    # secondAx1.plot(data['time'][minIndex-bound:minIndex+bound], data['EPtot'][minIndex-bound:minIndex+bound])

    # secondAx2.plot(data['time'][minIndex-bound:minIndex+bound], data['temp'][minIndex-bound:minIndex+bound])

    thirdFig = plt.figure()
    ax = thirdFig.add_subplot(111)
    ax.scatter(data['temp'], data['EPtot'], sizes, c=colors)

    if ZOOM_ON_MIN == True:
        if minIndex > 10:
            print("Will plot zoomed on min")
            zoomedFig = plt.figure()
            zax1 = zoomedFig.add_subplot(211)
            zTime = []
            zTemps = []
            zEPtot = []
            for i in range(minIndex - ZOOM_NUM, minIndex + ZOOM_NUM + 1):
                row = data.loc[i]
                zTime.append(row['time'])
                zTemps.append(row['temp'])
                zEPtot.append(row['EPtot'])
            zax1.plot(zTime, zEPtot, "blue")
            zax1.scatter([minTime], [minEnergy], 50, ["red"])

            zax2 = zoomedFig.add_subplot(212)
            zax2.plot(zTime, zTemps)
            zax2.scatter([minTime], [data.loc[minIndex]['temp']], 50, ["red"])
    

FRAME_DELTA = 500
outFrame = open("frames.out", 'w')
for i in range(0, len(mins)):
    print(mins[i])
    print(min_steps[i])
    correctedStep = min_steps[i]//FRAME_DELTA
    line = str(i) + ',' + "equil.mdcrd" + ',' + str(int(correctedStep)) + '\n'
    outFrame.write(line)

outFrame.close()
o = open('step.txt', 'w')
o.write(str(int(minStep/100)) + '\n')
o.close()

if SHOULD_PLOT == True:
    plt.show()