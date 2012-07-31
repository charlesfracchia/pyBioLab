"""
new_syringe_pumps.py

by Charles Fracchia, Copyright (c) 2012
based on syringe_pump.py library by Will Dickson (https://bitbucket.org/iorodeo/syringe_pump)

New Era 500 501 and 1000 Syringe Pump Device class
"""

from pybiolab import Device 
from pybiolab import SyringePump

class NESyringePump(Device,SyringePump):
    """docstring for NESyringePump"""
    def __init__(self,dId,destination,linkType,source,baud,synchronous):
        #Device specific
        brand = 'New Era'
        model = 'NE'
        modelNo = '500', '501', '1000'
        reference='http://www.syringepump.com/download/'
        notes='Call them to get the ZIP archives passwords'
        #Syringe Pump specific
        maxDiameter = 0.1       #mm
        minDiameter = 50        #mm
        #Command List
        self.commands = {
            'setDiameter':'DIA !diameter!',       #as float
            'getRate':'RAT',
            'setRate':'RAT !rate! !units!',
            'getVolume':'VOL',
            'setVolume':'VOL !volume! !units!',
            'clearVolume':'CLD !direction!',
            'getDirection':'DIR',
            'setDirection':'DIR !direction!',
            'getPhaseNumber':'PHN',
            'setPhaseNumber':'PHN !phaseData!',
            'run':'RUN',
            'stop':'STP',
            'getAlarmMode':'AL',
            'setAlarmMode':'AL !mode!',
            'getPowerFailMode':'PF',
            'setPowerFailMode':'PF !mode!',
            'getTTLTrigger':'TRG',
            'setTTLTrigger':'TRG !mode!',
            'getTTLDirectionControl':'DIN',
            'setTTLDirectionControl':'DIN !mode!',
            'getPumpMotorOperatingTTLOutput':'ROM',
            'setPumpMotorOperatingTTLOutput':'ROM !mode!',
            'getKeypadLockout':'LOC',
            'setKeypadLockout':'LOC !mode!',
            'getProgramEntryModeKeypadLockout':'LOC P',
            'setProgramEntryModeKeypadLockout':'LOC P !mode!',
            'getBeepMode':'BP',
            'setBeepMode':'BP !mode!',
            'getTTLOutput':'OUT !pin!',
            'setTTLOutput':'OUT !pin! !mode!',
            'getTTLInput':'IN !pin!',
            'getBuzzer':'BUZ',
            'setBuzzer':'BUZ !mode! !times!',
            'getPumpNetworkAddress':'*ADR',
            'setPumpNetworkAddress':'*ADR !address! !baudMode! !baud! !pumpMode!', #Address=[0:99], baudMode=['','B'], baudRate=[19200,9600,2400,1200,300], pumpMode=['DUAL','RECP'] ()
            'getSafeMode':'SAF',
            'setSafeMode':'SAF !timeout!', #timeout=[0:255]
            'getFirmwareVersion':'VER',
            'reset':'*RESET',
        }
        
        #Device Warnings
        #self.warnings
        
        #Initialise every parent class
        Device.__init__(self, dId, brand, model, modelNo, source, destination, linkType, True, baud, synchronous)
        SyringePump.__init__(self, minDiameter, maxDiameter)
    
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