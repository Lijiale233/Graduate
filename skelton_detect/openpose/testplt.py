import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib.ticker import FuncFormatter

xpoints = np.array([1, 8])
ypoints = np.array([3, 10])
filename = "1651577677.9304092txt"
data = []

with open("output/"+filename) as f:
    lines = f.readlines()
    for line in lines:
        line = (line[1:-2]).split(', ')
        data.append(line)

for i in range(2):
    if i ==0:
        data[i] = [int(x) for x in data[i]]
    if i == 1:
        data[i] = [-int(x) for x in data[i]]

xpoints = np.array(data[0])
ypoints = np.array(data[1])
sklName = data[2]

plt.axis('equal')
plt.plot(xpoints,ypoints, 'o')
plt.show()
