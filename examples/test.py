import time
from pybiolab.devices.newbrunswick.innova_44_44R import Innova_44_44R

dodo = Innova_44_44R(0,'00:13:A2:00:40:8B:D6:45','zigbee','/dev/tty.usbserial-A800HATZ',9600,False)

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

print "Setting RPM"
dodo.setRPM(200)
time.sleep(10)
print "Getting Settings"
dodo.getSettings()