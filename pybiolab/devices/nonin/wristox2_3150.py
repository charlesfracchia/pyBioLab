"""
wristox2_3150.py

by Charles Fracchia, Copyright (c) 2012

Nonin WristOx2 3150 Medical Oximeter Device class
"""

from pybiolab import Device 
from pybiolab import Oximeter

class WristOx2(Device,Oximeter):
    """docstring for WristOx2"""
    def __init__(self,dId,destination,linkType,source,baud,synchronous):
        #Device specific
        brand = 'Nonin'
        model = 'WristOx2'
        modelNo = '3150'
        #Medical Oximeter specific
        
        #Command List, used only for easy parsing reference
        self.commands = {
            'getPatientData':'MPB?',
            'cancelGetPatientData':'CAN!',
            'deletePatientData':'MCL!',
            'setBluetoothTimeout':'SBT=!minutes!',      #minutes=[0-255]
            'getDateTime':'DTM?',
            'setDateTime':'DTM=!YY!!MM!!DD!!hh!!mm!!ss!',
            'getConfiguration':'CFG?',
        }
        #Responses
        self.responses = {
            'getPatientData':'\x06\xFE\xFD\xFB!restOfData!'
        }
        
        #Initialise every parent class
        Device.__init__(self, dId, brand, model, modelNo, source, destination, linkType, True, baud, synchronous)
        Oximeter.__init__(self)
    
    def decodeData(self):
        """Decodes the data"""
        pass
        print "hello this is a test"
    
    def parseResponse(self):
        """docstring for fname"""
        pass
        print 'Monkey tickles a pig backwards'
        