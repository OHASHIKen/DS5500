import ds5500
import time 
import ROOT 
import math
import numpy

########### root histogram 
#Can = ROOT.TCanvas("Can", "Can", 800, 1000)
#hist = ROOT.TH1F("hist", "scintillator1; Integrated Pulse Intensity [V]; Events", 50, 0., 20)
#hist2 = ROOT.TH1F("hist2", "; Integrate Pulse Intensity [p.e.]; Events", 50, 0., 50)


########### setting for integrated values 
i = 0
y_pre = 0.
attempts = 3600*5
# integral_lower = 0
# integral_upper = 1E-7
integral_lower = -5E-8
integral_upper = 2E-7

channel_number = 1 ## channel to be read 
trigger_channel = 1 ## channel number for trigger 

###########  constant
# PointsPerDiv = 5000
# NumberOfPointsToRead = 1000 # 1000
# TimeOffset = 2E-8 # -100
NumberOfPointsToRead = 1000
TimeOffset = 0 # -100
# vdiv = 1E-1
vdiv = 1E-1 ##縦軸１ブロックの大きさ
voffset = 0
# tdiv = 1E-7 ##横軸1ブロックの大きさ
tdiv = 1E-7
trigger = -0.2
samplingrate = 1E+9 ## number of samples in one second
tsleep = 1


### connect to oscilloscope 
ds = ds5500.DS5500("192.168.8.11", "5198", 3000)

### set horizontal/vertical range O
ds.SetTimeDiv(tdiv) ## 100 ns/div
ds.SetVerticalDiv("C{}".format(channel_number),vdiv) ## 50 mV/div
ds.SetOffset("C{}".format(channel_number), voffset) ## set offset for CH1 to -150 mv.

### trigger related
ds.GetTriggerMode()
ds.SetTriggerSource("CH{}".format(trigger_channel))
ds.SetTriggerSlope("NEG")
ds.SetTriggerLevel(trigger) ## 100 mV threshold

### to read wave format 
ds.SetNumberOfPoints(NumberOfPointsToRead)
ds.SetStartPoint(TimeOffset)

### read wave
ds.SetWaveFormSource('CH{}'.format(channel_number))
ds.PrintValuesForWaveForm()
#print(ds.inst.query('WAVESRC?'))


################# loop : get wave form and the integrated value
while i < attempts:
    i = i + 1
 
    # Trigger mode set to SINGLE and RUN
    ds.inst.write('*TRG')
    time.sleep(0.001)
    
    # Check the trigger detection
    while True:
        stat = ds.inst.query('TESR?')
        if (stat == '+0000001'):
            break
        else:
            time.sleep(0.01)

    # Read data
    time.sleep(0.01)
    integral = [0., 0., 0., 0.]
    
    for ch in range(4):
        ds.SetWaveFormSource("CH{}".format(ch+1))
        xaxis, yaxis = ds.GetCurrentWaveForm()
        if yaxis.size != NumberOfPointsToRead:
            print('Error: size of data was not correct.')
            
        min_value = 10.
        integrated_value = 0.
        for j in range (NumberOfPointsToRead):
            if (xaxis[j] > integral_lower) and (xaxis[j] < integral_upper):
                integrated_value += yaxis[j]
            if min_value > yaxis[j]:
                min_value = yaxis[j]
        integral[ch] = integrated_value

    print('Event {} {:.3f}  {:.6f}  {:.6f}  {:.6f}  {:.6f}'.format(i, 
                                                               time.time(),
                                                               integral[0], 
                                                               integral[1], 
                                                               integral[2], 
                                                               integral[3]), flush=True)



######## after loop
#Can.Divide(1,2)

#Can.cd(1)
#hist.Draw("")
#hist.SetLineColor(ROOT.kRed)
#hist.SetLineWidth(3)

#Can.cd(2)
#hist2.Draw("")
#hist2.SetLineColor(ROOT.kRed)
#hist2.SetLineWidth(3)

#Can.Print("test_of_scintillator1.pdf")

######## end of the code 
del ds
