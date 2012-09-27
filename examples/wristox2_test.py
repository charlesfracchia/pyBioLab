import time
from pybiolab.devices.nonin import WristOx2
#00:13:A2:00:40:8B:D6:45
dodo = WristOx2(0,'00:13:A2:00:40:8B:D6:45','serial','/dev/tty.Nonin_Medical_Inc_31301',9600,False)

#print dodo.id
#print dodo.brand
#print dodo.model
#print dodo.modelNo
#print dodo.maxSpeed
#print dodo.minTemp
#print dodo.maxTemp
#print dodo.destination.encode('hex')
#print dodo.baud
#print dodo.linkType

#print "Setting RPM"
#dodo.setRPM(200)
#time.sleep(10)
#print "Setting RPM to 250"
#dodo.sendCommand('setRPM',rpm=250)
#time.sleep(20)
print "Setting RPM to 100"
#dodo.sendCommand('getFirmwareVersion')
dodo.sendCommand('setRPM',rpm=100)

dodo.sendCommand('getDateTime')
#dodo.getSettings()