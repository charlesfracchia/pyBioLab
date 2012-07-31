"""
phd_ultra.py

by Charles Fracchia, Copyright (c) 2012

Harvard Apparatus PHD Ultra Syringe Pump Device class
"""

from pybiolab import Device 
from pybiolab import SyringePump

class PHDUltra(Device,SyringePump):
    """docstring for PHDUltra"""
    def __init__(self,dId,destination,linkType,source,baud,synchronous):
        #Device specific
        brand = 'Harvard Apparatus'
        model = 'PHD Ultra'
        modelNo = ''
        reference='https://www.harvardapparatus.com/hapdfs/HAI_DOCCAT_4/703005_PHD_ULTRA_Manual.pdf'
        #Syringe Pump specific
        maxDiameter = 0.1       #mm
        minDiameter = 50        #mm
        #Command List
        self.commands = {
            'getAddress':'address',
            'setAddress':'address !address!',       #address = [0:99]
            'getBaud':'baud',
            'setBaud':'baud !baud!',
            'displayStoredMethod':'cat !baud!',     #baud = ['9600','19200','38400','57600','115200']
            'getDisplayBrightness':'dim',
            'setDisplayBrightness':'dim !percent!',     #percent = [0:100]
            'getEchoState':'echo !percent!',
            'setEchoState':'echo !mode!',       #mode = ['on','off']
            'getFreeSteps':'free',
            'getInfusionForce':'force',
            'setInfusionForce':'force !percent!',
            'getPromptModeState':'poll';
            'getPromptModeState':'poll !mode!';
            'getDateTime':'time',
            'getDateTime':'time !month!/!day!/!year! !hours!:!minutes!:!seconds!',
            'getValveState':'valve',
            'setValveState':'valve !mode!',
            'getValveDutyCycle':'vduty',
            'setValveDutyCycle':'vduty !percent!',
            'getShortVersion':'ver',
            'getFirmwareVersion':'version',
            #Run commands
            'runInfuse':'irun',
            'runWithdraw':'wrun',
            'runReverse':'rrun',
            'run':'run',
            'stop':'stop',
            #Rate commands
            'getCurrentRate':'crate',
            'getDiameter','diameter',
            'setDiameter','diameter !diameter!',
            'getRampInfusionRate','iramp',
            'setRampInfusionRate','iramp !startRate! !startRateUnits! !endRate! !endRateUnits! !rampTime!',     #rampTime in seconds
            'getInfusionRate':'irate',
            'setInfusionRate':'irate !rate! !rateUnits!',
            'getRampWithdrawRate','wramp',
            'setRampWithdrawRate','wramp !startRate! !startRateUnits! !endRate! !endRateUnits! !rampTime!',     #rampTime in seconds
            'getWithdrawRate':'wrate',
            'setWithdrawRate':'wrate !rate! !rateUnits!',
            #Volume commands
            'clearInfusedVolume':'civolume',
            'clearTargetVolume':'ctvolume',
            'clearBothVolumes':'cvolume',
            'clearWithdrawnVolume':'cwvolume',
            'getInfusedVolume':'ivolume',
            'getTargetVolume':'tvolume',
            'setTargetVolume':'tvolume !volume! !volumeUnits!',
            'getWithdrawnVolume':'wvolume',
            #Time commands
            'clearInfusedTime':'citime',
            'clearBothTimes':'ctime',
            'clearTargetTime':'cttime',
            'clearWithdrawnTime':'cwtime',
            'getInfusedTime':'itime',
            'getTargetTime':'ttime',
            'setTargetTime':'ttime !time! !timeUnits!',
            'getWithdrawnTime':'wtime',
            #Digital I/O commands
            'getTriggerInputPortStatus':'input',
            'setOutputPortLevel':'output !port! !level!',       #port=[1,2] level=['high','low']
            'setSyncPortLevel':'sync !level!',
            #Maintenance
            'getDeviceStatus':'status'
        }
        
        #Device Warnings
        #self.warnings
        
        #Initialise every parent class
        Device.__init__(self, dId, brand, model, modelNo, source, destination, linkType, True, baud, synchronous)
        SyringePump.__init__(self, minDiameter, maxDiameter)