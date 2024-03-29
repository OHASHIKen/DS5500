import ds5500
import time
from matplotlib import pyplot

## settings for integral
i = 0
y_pre = 0.
attemps = 4 # 100
integral_lower = 0
integral_upper = 1E-7
### constant
# PointsPerDiv = 5000
NumberOfPointsToRead = 100 # 1000
TimeOffset = 0 # -100
# vdiv = 1E-1
vdiv = 1E-2 ##縦軸１ブロックの大きさ
voffset = -0.03
tdiv = 1E-7 ##横軸1ブロックの大きさ
trigger = 6E-3
samplingrate = 1E+9 ## number of samples in one second
tsleep = 4 ## sleep する時間



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
ds.SetCurrentSamplingRate(samplingrate)

### read wave
ds.SetWaveFormSource("CH1")
ds.PrintValuesForWaveForm()


while i < attemps:
    xaxis, yaxis = ds.GetCurrentWaveForm()
    print(i)
    print(xaxis)
    print(yaxis)
    if yaxis.size == 0:
        time.sleep(tsleep)
        xaxis, yaxis = ds.GetCurrentWaveForm()
        print(yaxis)
    integrated_value = 0.
    for j in range (ds.numberOfPointsToRead):
        if (xaxis[j] > integral_lower) and (xaxis[j] < integral_upper):
            integrated_value += yaxis[j]
    y = integrated_value
    print(y)
    
    if y == y_pre:
        y_pre = y
    
    else:
        y_pre = y
        # i += 1
    i += 1
    
    time.sleep(tsleep)

del ds
