import ds5500
import time

## settings for integral
i = 0
y_pre = 0.
attemps = 100
integral_lower = 0
integral_upper = 1E-7
### constant
# PointsPerDiv = 5000
NumberOfPointsToRead = 1000 # 1000
TimeOffset = 0 # -100
# vdiv = 1E-1
vdiv = 1E-2 ##縦軸１ブロックの大きさ
voffset = -0.03
tdiv = 1E-7 ##横軸1ブロックの大きさ
trigger = 6E-3
samplingrate = 1E+9 ## number of samples in one second


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
ds.SetCurrentSampingRate(samplingrate)

### read wave
ds.SetWaveFormSource("CH1")
ds.PrintValuesForWaveForm()


while i < attemps:
    y = ds.GetIntegratedValue(limit_low = integral_lower, limit_high = integral_upper)
    if y == y_pre:
        y_pre = y
    
    else:
        print("Attempts {0} : integrated value {1}".format(i, y))
        y_pre = y
        i += 1
    
    time.sleep(4)


