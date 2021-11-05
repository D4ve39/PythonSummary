import numpy as np
import matplotlib.pyplot as plt

# %% Plot Multimeter Data
measurements = np.array([3.15, 4.12, 9.92])

x = np.array([1.5, 2, 5])
y = np.array([3, 4, 10])

plt.figure()
plt.plot(x, measurements, label="Measurements")
plt.plot(x, y, label="Ideal")
plt.xlabel("Voltage [V]", fontsize=22)
plt.ylabel("Boosted Voltage [V]", fontsize=22)
plt.legend()
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()

plt.figure()
plt.plot(2*x/10*15, (y-measurements)/10*15)
plt.ylabel("Deviation in position [um]", fontsize=22)
plt.xlabel("Desired position [um]", fontsize=22)
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()

print("Difference in distance in um with current tolerance: ", (10-9.92)/10*15)

print("Difference in distance in um with current tolerance: ",(3-3.15)/10*15)

# %% Plot measurement data

T=150/24000
FILEPATH = "C:\\multimat\\experiment_results\\3D-Print_14-05-20_16-17\\z_measurement.csv" 
data = np.loadtxt(FILEPATH, delimiter=";")
x = [i*T for i in range(len(data[:,1]))]

plt.figure()
plt.plot(x, data[:,1])
plt.xlabel("time [s]")
plt.ylabel("z measurement [um]")
plt.grid(True)
plt.show()