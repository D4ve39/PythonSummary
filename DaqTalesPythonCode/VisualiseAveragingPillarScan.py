# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


FILEPATH = "C:/multimat/experiment_results/3D-Print_18-06-20_19-10_Bike2ndLast/AvScan.csv"
#FILEPATH = "C:/Users/david/polybox/multimat/experiment_results/3D-Print_18-06-20_19-10/AvScan.csv"
#FILEPATH = "C:/multimat/experiment_results/3D-Print_19-06-20_12-25/PillarScanHeight58.825000.csv"
THRESH = 0.5

Data = np.loadtxt(FILEPATH, delimiter=",")

V_raw = Data[0]
X = Data[1]
Y = Data[2]

#Processed Data

V_min = - np.max(V_raw)
V_max = - np.min(V_raw)
V_processed = (-V_raw - V_min)/(V_max - V_min)
V_processed[V_processed < THRESH] = 0

#Estimated pillar center
V_sum = np.sum(V_processed)
x_avv = np.dot(V_processed, X)/V_sum
y_avv = np.dot(V_processed, Y)/V_sum

#Plot raw data
fig = pyplot.figure("Raw measurement Values")
ax = Axes3D(fig)

ax.scatter(X, Y, V_raw)

#Draw a line with the estimated center
ax.plot(x_avv*np.ones((10,)), y_avv*np.ones((10,)), np.linspace(-V_max, -V_min, 10), color = "r")
ax.set_xlabel('x',fontweight ='bold')
ax.set_ylabel('y',fontweight ='bold')
ax.set_zlabel('Deflection voltage',fontweight ='bold')
ax.set_title('Raw measurement Values',fontweight ='bold')
pyplot.show()

#Plot 
fig = pyplot.figure("Transformed Measurement Values")
ax = Axes3D(fig)

ax.scatter(X, Y, V_processed)

ax.plot(x_avv*np.ones((10,)), y_avv*np.ones((10,)), np.linspace(0, 1.1, 10), color = "r")
ax.set_xlabel('x',fontweight ='bold')
ax.set_ylabel('y',fontweight ='bold')
ax.set_zlabel('Deflection voltage',fontweight ='bold')
ax.set_title('Transformed measurement Values',fontweight ='bold')
pyplot.show()