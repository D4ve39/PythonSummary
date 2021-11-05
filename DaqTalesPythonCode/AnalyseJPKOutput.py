# %%Load up Data
import numpy as np
import matplotlib.pyplot as plt
#from AnalyseVDeflOutput import getMaxFeedbackValues
FILE = "C:\\Users\\jerom\\polybox\\Shared\\20200513 JPK Osci\\approach_test1.out"
#FILE = "C:\\multimat\\JPKOutputs\\20200529 Test Wet Print\\wetpring_timeout_4s.out"
#FILE = "C:\\multimat\\JPKOutputs\\2020513 Test 2\\test2_approach_constant_v.out"
FILE = "C:\\multimat\\JPKOutputs\\20200604 WetPrint\\20200604 WetPrint\\3x3array_large.out"
FILE = "C:\\multimat\\JPKOutputs\\20200610 newDaisy\\20200610 newDaisy\\real-2020.06.10-09.22.22.out"
FILE = "C:/multimat/experiment_results/10-06-20_16-46_StepperCheck/steppercheck.out"
Data = np.loadtxt(FILE, delimiter=" ")

columns = {"time": 0, "x":1, "y":2, "z_nonmeasured":3, "z":4, "Vdefl":5}

#%% Make plots of x,y,z,Vdefl

samplerate = 1000
timespan = (None, None)

start = int(timespan[0]*samplerate) if not timespan[0] is None else None
end = int(timespan[1]*samplerate)if not timespan[1] is None else None

plt.figure()
plt.plot(Data[start:end,columns["time"]], Data[start:end,columns["x"]], label="x")
plt.xlabel("$time$")
plt.ylabel("$x [V]$")
plt.grid(True)
plt.title("x value")
plt.show()

plt.figure()
plt.plot(Data[start:end,columns["time"]], Data[start:end,columns["y"]], label="y")
plt.xlabel("$time$")
plt.ylabel("$y [V]$")
plt.grid(True)
plt.title("y value")
plt.show()

plt.figure()
plt.plot(Data[start:end,columns["time"]], Data[start:end,columns["z"]]/1000000, label="z")
plt.xlabel("$time$")
plt.ylabel("$z [um]$")
plt.grid(True)
plt.title("z value")
plt.show()

plt.figure()
plt.plot(Data[start:end,columns["time"]], Data[start:end,columns["Vdefl"]], label="Vdefl")
plt.xlabel("$time$")
plt.ylabel("$V_{defl}$")
plt.grid(True)
plt.title("Vdefl")
plt.show()

#AnalyseVDeflOutput.getMaxFeedbackValues(Data[:,columns["Vdefl"]])

fig, a = plt.subplots(2, 1, sharex=True)
a[0].plot(Data[start:end,columns["time"]], Data[start:end,columns["z"]]/1000000)
a[0].set_title("height (measured)")
a[1].plot(Data[start:end,columns["time"]], Data[start:end,columns["Vdefl"]])
a[1].set_title("Vdefl")
plt.show()

fig, a = plt.subplots(3, 1, sharex=True)
a[0].plot(Data[start:end,columns["time"]], Data[start:end,columns["x"]])
a[0].set_title("x")
a[1].plot(Data[start:end,columns["time"]], Data[start:end,columns["y"]])
a[1].set_title("y")
a[2].plot(Data[start:end,columns["time"]], Data[start:end,columns["z"]]/1000000)
a[2].set_title("height (measured)")
plt.show()
