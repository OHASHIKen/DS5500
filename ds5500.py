"""

Manual of commands : https://www.iti.iwatsu.co.jp/manual/pdf_j/digital_osc/ViewGo/viewgo2-rj-v1.pdf

"""
import pyvisa as visa
import numpy

class DS5500(object):
    def __init__(self, ip, port, timeout=1):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource("TCPIP::{0}::{1}::SOCKET".format(ip, port))
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self.timeout = timeout
        self.numberOfPointsToRead = 1000
        self.timeOffset = 0
        self.vDiv = 1E-2
        self.vOffset = 0
        self.tDiv = 1E-7
        self.Trigger = 6E-3
        self.samplingRate = 1E+9
        print(self.inst.query('*IDN?')) ## print oscilloscope name
        

    ### Basic setting ###
    def GetDate(self):
        print(self.inst.query("DATE?"))

    def SetDate(self, day, month, year, hour, minute, second):
        """
        SetDate(day, month, year, hour, minute, second)
        month : JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
        others should be integer value. 
        """
        self.inst.write("DATE {0},{1},{2},{3},{4},{5}".format(day, month, year, hour, minute, second))

    def SetOffset(self, trace, offset):
        """
        SetOffset(trace, offset)
        trace : C1, C2, C3, C4, M1
        offset : voltage
        """
        self.inst.write("{0}:OFST {1}".format(trace, offset))
        print("Offset changed. Current offset is {0}".format( self.inst.query("{0}:OFST?".format(trace)) ) )
        self.vOffset = offset
        
    def SetTimeDiv(self, value):
        """
        SetTimeDiv(value)
        example of value : +20.000000E-03 (20ms/div), 20US (20 micro sec/div), 1E-9 (1ns/div)
        """
        self.inst.write("TDIV {0}".format(value))
        self.tDiv = value
        print("Time/Div is set to {0}".format( self.inst.query("TDIV?")))

    def GetTimeDiv(self):
        tdiv = self.inst.query_ascii_values("TDIV?")
        return tdiv[0]
        
    def SetVerticalDiv(self, trace, v_gain):
        """ 
        Set vertical division 
        SetVerticalDiv(trace, v_gain)
        trace : C1, C2, C3, C4, M1
        v_gain : (vertical division) +5.0E-3 (5mV)
        """
        self.inst.write("{0}:VDIV {1}".format(trace, v_gain))
        self.vDiv = v_gain
        
    def GetVerticalDiv(self, trace):
        """
        Get value of vertical division
        GetVerticalDiv("C1")
        """
        # self.inst.write("{0}:VDIV?".format(trace))
        # vdiv = self.inst.read_raw()
        vdiv = self.inst.query_ascii_values("{0}:VDIV?".format(trace))
        print("Current Vertical Division for {0} : {1}".format(trace, vdiv))
        return vdiv[0]
        
    ### Display setting ###
    def SetDisplay(self, state):
        """
        Turn display ON/OFF 
        SetDisplay(state)
        state : ON or OFF
        """
        self.inst.write("DISP {0}".format(state))
        
        
    ### Trigger related ###
    def GetTriggerMode(self):
        print("Current trigger mode is {0}".format(self.inst.query('TRMD?')))
        
    def SetTriggerSource(self, ch):
        """
        Set channel of trigger source
        example: SetTriggerSource("CH1")
        """
        self.inst.write("TSRC {0}".format(ch))
        print("Trigger source is set to {0}".format(self.inst.query('TSRC?')))
        
    def SetTriggerSlope(self, slope):
        """
        Set trigger slope 
        SetTriggerSource("POS") or SetTriggerSource("NEG")
        """
        self.inst.write("TSLP {0}".format(slope))
        print("Trigger slope is set to {0}".format(self.inst.query('TSLP?')))
        
        
    def SetTriggerLevel(self, level):
        """
        Set trigger level.
        SetTriggerLevel(level)
        level : voltage in V
        """
        self.inst.write("TLVL {0}".format(level))
        self.Trigger = level
        print("Trigger level is set to {0}".format( self.inst.query('TLVL?')))

    def SetTriggerHoldTime(self, time):
        """ 
        Set Trigger hold time
        SetTriggerHoldTime(time)
        time : time in second
        """
        self.inst.write("THTM {0}".format(time))
        print("Set Trigger hold time to {0}".format( self.inst.query('THTM?')))
        
    def RunTrigger(self):
        """ 
        Change trigger mode to run 
        """
        self.inst.write('*TRG')
        
    def SetPeriodicTrigger(self, when, m):
        """ 
        Set periodic trigger
        SetPerioricTrigger(when, m)
        when : M_T or T_M
        m : (time) +40.000000E-09 (40ns)
        """
        self.inst.write('TPTM {0}, {1}'.format(when, m))
        
    def GetTriggerFrequency(self):
        """
        Get trigger frequency
        """
        return self.inst.query("FRQCNT?")
    
    ### Auto measurements setting ###
    def SetAutoMeasurementsMode(self, modeid):
        """
        Basic setting of auto measurements.
        SetAutoMeasurementsMode(self, modeid)
        modeid : A, B, C, D
        """
        self.inst.write("DIRM {0}".modeid)
        print("# of auto measurements : {0}".format(self.inst.query("DIRM?")))
        
        
    def SetAutoMeasurements(self, channel, mode):
        """
        Set auto measurements mode
        SetAutoMeasurements(channel, mode)
        channel : OFF, CH1, CH2, CH3, CH4, MATH
        mode : AX, MIN, P-P, VRMS, CVRMS, VMEAN, CVMEAN, TOP, BASE, T-B, +OSHOT, 
        -OSHOT, TR20-80, TF80-20, TR10-90, TF 90-10, FREQ, PERIOD, +PULSE, -PULSE, 
        +WIDTH, -WIDTH, DUTY, INTEGRAL, SKEW, DELTAT
        """
        self.inst.write("MSEL {0}, {1}".format(channel, mode))
        print("Auto measurements mode : {0}".format( self.inst.query('MSEL?')))
        
    def SetAutoMeasurementsDetail(self, level1, slope1, source2, level2, slope2):
        """
        Set source, level, and slope for auto measurements
        SetAutoMeasurementsDetail(level1, slope1, source2, level2 slope2)
        level : value from 10 to 90.
        slope : RISE or FALL
        source2 : CH1, CH2, CH3, Ch4
        """
        self.inst.write("SKLV {0}, {1}, {2}, {3}, {4}".format(level1, slope1, source2, level2, slope2))
        print("Auto measurements setting : {0}".format( self.inst.query('SKLV?')))


    ### Date transforming ###
    def SetDataOrder(self, order):
        """
        SetDataOrder(order)
        order: H/L or L/H 
        H/L : send upper bytes first 
        L/H : send lower bytes first
        """
        self.inst.write('{0}'.format(order))

    def SetDataType(self, datatype):
        """
        Set data format read by GetWaveForm()
        data type : ASCII, BYTE, WORD
        """
        self.inst.write('DTFORM {0}'.format(datatype))

    ### get wave form ###
    def SetWaveFormSource(self, channel):
        """
        Set Source of wave form 
        SetWaveFormSource(channel)
        channel : CH1, CH2, CH3, CH4, MATH
        """
        self.inst.write('WAVESRC {0}'.format(channel))

    def SetStartPoint(self, offset):
        """
        Set start points
        SetStartPoints(offset)
        """
        self.inst.write('DTSTART {0}'.format(offset))
        self.timeOffset = offset 
        
    def SetNumberOfPoints(self, points):
        """
        Set number of points to be read 
        SetNumberOfPoints(points)
        """
        self.inst.write('DTPOINTS {0}'.format(points))
        self.numberOfPointsToRead = points
        
    def GetWaveForm(self):
        """
        Get waveform 
        """
        self.SetDataType('ASCII')
        data = self.inst.query_ascii_values('DTWAVE?', container=numpy.array )
        # data = self.inst.read() 
        return data

    def SetCurrentSamplingRate(self, samplingrate):
        self.samplingRate = samplingrate
        
    def PrintValuesForWaveForm(self):
        print("Please compare following values with Oscilloscope!!\n")
        print("Time div : {}\n".format(self.tDiv))
        print("Time offset : {}\n".format(self.timeOffset))
        print("vertical div : {}\n".format(self.vDiv))
        print("vertical offset : {}\n".format(self.vOffset))
        print("Trigger level : {}\n".format(self.Trigger))
        print("Sampling Rate : {}\n".format(self.samplingRate))
        print("number of points for wave form : {}\n".format(self.numberOfPointsToRead))
        print(self.inst.query('DTINF?'))

    def GetCurrentWaveForm(self):
        """
        Get current waveform. 
        xaxis: time,
        yaxis: voltage
        """
        data = self.GetWaveForm() ## data points 
        conversion = self.vDiv/256/32
        
        ## ASCII 数値÷256÷32×電圧レンジ-オフセット値
        yaxis = conversion*data - self.vOffset
        #print(data)
        #print(conversion)

        ### xaxis 
        timeInit = - self.tDiv * 5 + self.timeOffset/self.samplingRate  ## -tdiv * 5
        timeEnd = - self.tDiv * 5 + (self.numberOfPointsToRead - self.timeOffset)/self.samplingRate
        xaxis = numpy.linspace( timeInit, timeEnd, self.numberOfPointsToRead) ## xaix 
        
        return xaxis, yaxis
    
    # def GetIntegratedValue(self, limit_low, limit_high):
    #     x, y = self.GetCurrentWaveForm()
    #     print("size of x and y axis : {0}, {1} ".format(x.size,y.size))
        
    #     integrated_value = 0
    #     for i in range(self.numberOfPointsToRead):
    #         if x[i] > limit_low and x[i] < limit_high:
    #             print(i)
    #             integrated_value += y[i]
                
    #     return integrated_value
    
    # def GetWaveInfo(self):
    #     info = self.inst.query_ascii_values('DTINF?')
        
    ### For quick check, plot a wave form ###
    

    
    ### wave form analysis ###
    
