
import ds5500

ds = ds5500.DS5500("192.168.8.11", "5198")
ds.SetNumberOfPoints(100)
data = ds.GetWaveForm()
print(data)

### trigger related
ds.GetTriggerMode()
ds.SetTriggerSource("CH1")
ds.SetTriggerSlope("POS")
ds.SetTriggerLevel(0.1)

ds.GetTriggerFrequency()

del ds
