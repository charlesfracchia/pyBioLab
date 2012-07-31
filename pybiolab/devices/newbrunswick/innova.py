"""
innova.py

by Charles Fracchia, Copyright (c) 2012

New Brunswick Innova 44/44R Shaking Incubator Device class
"""

from pybiolab import Device 
from pybiolab import Shaker
from pybiolab import Temperature

class Innova(Device,Shaker,Temperature):
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
        
        #Command List, used only for easy parsing reference
        self.commands = {
            'setRPM':'CS !rpm!',
            'setTemp':'CT !temp!',
            'setGrowLamp':'CL !mode!',      #mode = [0,1]
            'setUVLamp':'CU !mode!',
            'getFirmwareVersion':'RI',
            'getParameters':'RP',
            'getSetValues':'RS',
            'getCurrentValues':'RV',
            'getDateTime':'?D',
            'setDateTime':'=D !hours! !minutes! !seconds! !year! !month! !date! !day!',     #year=[00:99] day=[1:7]
        }
        #Responses
        self.responses = {
            'getParameters':'!rpm!\t!temp!\t!humidity!\t!co2!\t!growLamp!\t!uvLamp!',
            'setRPM':'CS !rpm!',
        }
        
        #Initialise every parent class
        Device.__init__(self, dId, brand, model, modelNo, source, destination, linkType, True, baud, synchronous)
        Shaker.__init__(self, maxSpeed)
        Temperature.__init__(self, minTemp, maxTemp)