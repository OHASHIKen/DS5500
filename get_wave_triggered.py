import ds5500
import time 
import ROOT 
import math
import numpy
from array import array
import datetime

########### for date and time
dt_now = datetime.datetime.now()

########### root output file 
f = ROOT.TFile("data_Cont0.9V/FC{}.root".format(dt_now.strftime('%Y%m%d-%H%M')) 
               , "RECREATE")
tree = ROOT.TTree("FrontCounter", "Integrated palse")

CH0 = array('f', [0.])
CH1 = array('f', [0.])
CH2 = array('f', [0.])
CH3 = array('f', [0.])

tree.Branch("CH0", CH0, 'CH0/F')
tree.Branch("CH1", CH1, 'CH1/F')
tree.Branch("CH2", CH2, 'CH2/F')
tree.Branch("CH3", CH3, 'CH3/F')



########### setting for integrated values 
i = 0
y_pre = 0. 
# attempts = 3600*5
# attempts = 300
attempts = 3000
# attempts = 6000
# attempts = 1500
# attempts = 30

# integral_lower = 0
# integral_upper = 1E-7
integral_lower = -8E-8
integral_upper = 2E-8

channel_number = 1 ## channel to be read 
trigger_channel = 4 ## channel number for trigger 

###########  constant
# PointsPerDiv = 5000
# NumberOfPointsToRead = 1000 # 1000
# TimeOffset = 2E-8 # -100
# NumberOfPointsToRead = 1000
NumberOfPointsToRead = 200
NumberOfChannelToRead = 3
TimeOffset = 0 # -100
# vdiv = 1E-1
vdiv = 2E-2 ##縦軸１ブロックの大きさ
voffset = 0
# tdiv = 1E-7 ##横軸1ブロックの大きさ
tdiv = 2E-8
trigger = -0.5
samplingrate = 1E+9 ## number of samples in one second
tsleep = 1


### connect to oscilloscope 
ds = ds5500.DS5500("192.168.8.11", "5198", 3000)

### set horizontal/vertical range O
ds.SetTimeDiv(tdiv) ## 100 ns/div
# ds.SetVerticalDiv("C{}".format(channel_number),vdiv) ## 50 mV/div
# ds.SetOffset("C{}".format(channel_number), voffset) ## set offset for CH1 to -150 mv.
for ch in range(3):
    ds.SetVerticalDiv("C{}".format(ch +1),vdiv) ## set vertical division.
    ds.SetOffset("C{}".format(ch+1), voffset) ## set offset 

# ###### for channel 4 
# ds.SetVerticalDiv("C{}".format(4),0.5) ## 500 mV/div
# ds.SetOffset("C{}".format(4), voffset) ## set offset for CH4




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
    
    for ch in range(NumberOfChannelToRead):
        ds.SetWaveFormSource("CH{}".format(ch+1))
        xaxis, yaxis = ds.GetCurrentWaveForm()
        # print(xaxis)
        if yaxis.size != NumberOfPointsToRead:
            print('Error: size of data was not correct. (channel {})'.format(ch))
            
        min_value = 10.
        integrated_value = 0.
        for j in range (NumberOfPointsToRead):
            if (xaxis[j] > integral_lower) and (xaxis[j] < integral_upper):
                integrated_value += yaxis[j]
            if min_value > yaxis[j]:
                min_value = yaxis[j]
        integral[ch] = integrated_value
        # print(integrated_value)
        # with open("log_axis_and_integrated_value.txt", "a") as f:
        #     numpy.savetxt(f, xaxis)
        #     numpy.savetxt(f, yaxis)
        #     f.write("\nintegrated value from {:.4f} to {:.4f} : {:.6f}".format( integral_lower, 
        #                                                                         integral_upper, 
        #                                                                         integrated_value))
    # CH0[0] = integral[0]
    CH1[0] = integral[0]## oscilloscope CH1
    CH2[0] = integral[1]## oscilloscope CH2
    CH3[0] = integral[2]## oscilloscope CH3
    tree.Fill()
    print('Event {} {:.3f} FC CH1 {:.6f} CH2 {:.6f} CH3 {:.6f}'.format(i, 
                                                                       time.time(),
                                                                       CH1[0],
                                                                       CH2[0],
                                                                       CH3[0]), flush=False)
    # print('Event {} {:.3f}  {:.6f}  {:.6f}  {:.6f}  {:.6f}'.format(i, 
    #                                                            time.time(),
    #                                                            integral[0], 
    #                                                            integral[1], 
    #                                                            integral[2], 
    #                                                            integral[3]), flush=True)



######## after loop
tree.Write("", ROOT.TObject.kOverwrite);
f.Close()

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
