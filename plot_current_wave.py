import ds5500
from matplotlib import pyplot
import numpy as np

### constants
PointsPerDiv = 5000
NumberOfPointsToRead = 100 # 1000
TimeOffset = 0 # -100
# vdiv = 1E-1
vdiv = 2E-3
voffset = 0
tdiv = 5E-8
trigger = 4E-2
samplingrate = 2E+9 ## number of samples in one second

### connect to oscilloscope 
ds = ds5500.DS5500("192.168.8.11", "5198", 3000)

### set horizontal/vertical range
ds.SetTimeDiv(tdiv) ## 50 ns/div
ds.SetVerticalDiv("C1",vdiv) ## 100 mV/div
ds.SetOffset("C1", voffset) ## set offset for CH1 to 0 mv.

### trigger related
ds.GetTriggerMode()
ds.SetTriggerSource("CH1")
ds.SetTriggerSlope("POS")
ds.SetTriggerLevel(trigger) ## 40 mV threshold

### to read wave format 
ds.SetNumberOfPoints(NumberOfPointsToRead)
ds.SetStartPoint(TimeOffset)

### read wave
ds.SetWaveFormSource("CH1")
data = ds.GetWaveForm() ## data points 
conversion = vdiv/256/32
## ASCII 数値÷256÷32×電圧レンジ＋オフセット値
yaxis = conversion*data  + voffset
print(data)
print(conversion)
print(yaxis)

### xaxis 
timeInit = TimeOffset/samplingrate
timeEnd = (NumberOfPointsToRead - TimeOffset)/samplingrate
xaxis = np.linspace( timeInit, timeEnd, NumberOfPointsToRead) ## xaix 

### plot 
pyplot.plot(xaxis, yaxis)
pyplot.show()
