"""
innova_44_44R.py

by Charles Fracchia, Copyright (c) 2012

New Brunswick Innova 44/44R Shaking Incubator Device class
"""

from pybiolab import Device 
from pybiolab import Shaker
from pybiolab import Temperature

class Innova_44_44R(Device,Shaker,Temperature):
    """docstring for Innova_44_44R"""
    def __init__(self,dId,destination,linkType,source,baud,synchronous):
        #Device specific
        brand = 'New Brunswick'
        model = 'Innova'
        modelNo = '44', '44R'
        #Shaker specific
        maxSpeed = 400
        #Temperature Specific
        minTemp = 4
        maxTemp = 80
        
        #Initialise every parent class
        Device.__init__(self, dId, brand, model, modelNo, source, destination, linkType, baud, synchronous)
        Shaker.__init__(self, maxSpeed)
        Temperature.__init__(self, minTemp, maxTemp)
        
    def setRPM(self,rpm):
        """Sets the [rpm] for the shaker"""
        pass
        #Command input by user
        #CS !rpm! !cr!
        command = b'\x43\x53\x20'   #'CS '
        rpmArg = str(rpm)           #rpm variable
        
        #Send
        sendCmd = self.send(command)    #Send 'CS '
        sendArg = self.send(rpmArg)     #Send rpm variable
        sendCR = self.send(b'\x0D')     #Send carriage return
        
        #Device specific warnings
        if(rpm >= 275):
            print "WARNING: When RPM > 275, 2L Erlenmeyer flasks have a tendency to slowly ease out of their clamps. This could lead them to shatter."
            
    def getSettings(self):
        """Returns the settings set on the device"""
        pass
        #Command input by user
        #RV !cr!
        command = b'\x52\x56'       #'RV'
        
        #Send
        sendCmd = self.send(command)    #Send 'CS '
        sendCR = self.send(b'\x0D')     #Send carriage return
    
    def _gotFrame(self,data):
        """
        Parse the received packed. This funciton is called asynchronously when the device.source (xbee or zigbee) receives a packet
        Return the received packet
        Acceptable:
            XBee.response object
        """
        pass
        try:
            
            frameType = '\t***%s***' % data['id']
            if data['id']=='tx_status':
                if data['deliver_status']=='\x25': print frameType,'\tRoute Not Found'
                if data['deliver_status']=='\x00': print frameType,'\tSuccess'
    
            elif data['id']=='at_response':
                print "\t\t%s\t(%s)" % (data['parameter']['node_identifier'],data['parameter']['source_addr_long'].encode('hex'))
            else:
                print data
        except KeyError:
            print 'Key Error'