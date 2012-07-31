import time
from pybiolab.devices.newera import NESyringePump
#00:13:A2:00:40:8B:D6:45
alpha = NESyringePump(0,'00:13:A2:00:40:7E:0F:18','zigbee','/dev/tty.usbserial-A800HATZ',9600,False)
#alpha.source.at(command="bd",parameter="\x04")
alpha.sendCommand('getFirmwareVersion')
alpha.sendCommand('setBuzzer',mode=1,times=6)