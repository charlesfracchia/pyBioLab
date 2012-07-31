"""
wristox2_3150.py

by Charles Fracchia, Copyright (c) 2012

Nonin WristOx2 3150 Medical Oximeter Device class
"""

from pybiolab import Device 
from pybiolab.medical import Oximeter

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
        }
        #Responses
        self.responses = {
            'getParameters':'!rpm!\t!temp!\t!humidity!\t!co2!\t!growLamp!\t!uvLamp!',
            'setRPM':'CS !rpm!',
        }
        
        #Initialise every parent class
        Device.__init__(self, dId, brand, model, modelNo, source, destination, linkType, True, baud, synchronous)
        Oximeter.__init__(self)