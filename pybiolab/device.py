"""
device.py

by Charles Fracchia, Copyright (c) 2012

Device class module

This class defines data and methods common to all devices. It is the base class for every type of device.
"""
import serial
from xbee import XBee, ZigBee
import httplib, urllib
import re
from timeout import *

allBaud = [300,1200,2400,4800,9600,14400,19200,28800,38400,57600,115200,230400]
#Types of supported connections
allSources = ['xbee','zigbee','http']

class Device(object):
    """docstring for Device"""
    
    def __init__(self, dId, brand, model, modelNo, source, destination, linkType, baud=9600, synchronous=True):
        #super(Device, self).__init__()
        self.id = dId
        self.brand = brand
        self.model = model
        self.modelNo = modelNo
        self.synchronous = synchronous
        self.linkType = self._checkLink(linkType)
        self.destination = self._checkDestination(destination)
        self.baud = self._checkBaud(baud)
        self.source = self._checkSource(source, baud, synchronous)
    
    def send(self,command):
         """
         Send a [command] to the device. Optionally you can set the [source] through which the command will be sent
         Return the raw result of the command, this is processed downstream byt the specific device code
         Acceptable:
             command as string
             source as an object of type XBee or ZigBee
         """
         pass
         destination = self.destination
         #Set dest_addr to xFFxFE because in DigiMesh firmware 16bit addresses are not used
         #and the field is changed to Reserved. In future, a full DigiMesh class should
         #probably be created to accommodate for further possible changes in the DM firmware
         self.source.tx(dest_addr_long=destination,dest_addr=b'\xFF\xFE',data=command)
         
         if (self.synchronous==True):
            response = self.source.wait_read_frame()
            return response
         else:
            return None
            
    def _checkBaud(self, baud):
        """
        Check that supplied [self.baud] rate is a valid baud
        Return the baud as int
        Acceptable (as int):
            300, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200 or 230400
        """
        pass
        if baud not in allBaud:
            print 'Invalid baud rate supplied. Will use preferred default value: 9600.'
            print 'Acceptable baud values: %s' % allBaud
            baud = 9600
            
        return baud

    def _checkLink(self, linkType):
        """
        Check that the supplied [linkType] is valid.
        Return lowercase string of the connection type ('xbee', 'zigbee' or 'http')
        Acceptable (in any capitalised/lower case state):
            XBee
            ZigBee
            HTTP
        """
        pass
        linkError = 'ERROR: Invalid connection type / link supplied. You need to supply a string with one of the following values: %s. Supplied: %s' % (allSources, linkType)
        if(type(linkType) == type(str())):
            loweredLink = linkType.lower()
            if(loweredLink not in allSources):
                print linkError
            else:
                return loweredLink
        else:
            print linkError
        
    def _checkDestination(self, destination):
        """
        Check that the [destination] is a valid address. 
        Return destination address if correct, Nothing otherwise. If it is a MAC address it will return it as a byte field (xAAxBBxCCxDDxEExFFxGGxHH)
        Acceptable: 
            XBee MAC address formatted like AA:BB:CC:DD:EE:FF:GG:HH:GG:HH
            IP address formatted like 000.000.255.255, each block has to be 0 <= n < 256
        """
        pass
        macRegex = '^[a-fA-F0-9][aceACE02468][:|\-]?([a-fA-F0-9]{2}[:|\-]?){4}[a-fA-F0-9]{2}$' #For regular mac addresses, not used but never know :)
        beeMACRegex = '^[a-fA-F0-9][aceACE02468][:|\-]?([a-fA-F0-9]{2}[:|\-]?){6}[a-fA-F0-9]{2}$'
        ipRegex = '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        
        if(self.linkType in ['xbee','zigbee']):
            regex = beeMACRegex
        elif(self.linkType == 'http'):
            regex = ipRegex
        else:
            print 'ERROR: Invalid connection type. Type has to be %s. Supplied: %s' % (allSources,self.linkType)
            regex=''
            
        found = re.compile(regex).search(destination)
        if(found):
            #Cast the MAC into a byte array (\xAA\xBB\xCC\xDD\xEE\xFF\xGG\xHH)
            return destination[found.start():found.end()].replace(':','').decode('hex')
        else:
            if(self.linkType in ['xbee','zigbee']):
                print 'ERROR: Invalid destination MAC address supplied. Format expected: AA:BB:CC:DD:EE:FF:GG:HH'
            elif(self.linkType == 'http'):
                print 'ERROR: Invalid destination IP address supplied. Format expected: AAA.AAA.AAA.AAA'
                
    def _checkSource(self, source, baud, synchronous):
        #could check to list the available com ports on the machine and check against that...
        """
        Check that the connection [source] string is acceptable and instanciate the Bee object
        Return the object source: XBee(Serial(source))
        Accepted types: 
            /dev/tty.*
            COM*
            http://
            https://
        """
        pass
        #Warn if source is being set with different
        if (baud != self.baud):
            print 'WARNING: You are setting a source with a different baud rate than your destination device (lab equipment). \
            This will prevent you from communicating (and sending commands) to the device you are trying to control. \
            Source: %s and Destination: %s' % (baud,self.baud)
        
        #XBee & ZigBee
        if (self.linkType in ['xbee','zigbee']):
            foundUnixCOM = re.findall(r'(/dev/tty.\S+)', source)
            foundWinCOM = re.findall(r'(COM.\S+)', source)
            if (len(foundUnixCOM)==1 or len(foundWinCOM)==1):
                if (self.linkType == 'xbee'):
                    try:
                        if (synchronous==False): source = XBee(serial.Serial(source,baud), callback=self._gotFrame)
                        else: source = XBee(serial.Serial(source,baud))
                    except serial.SerialException:
                        print "WARNING: Could not open the provided XBee's source serial port (%s)" % source
                elif (self.linkType == 'zigbee'):
                    try:
                        if (synchronous==False): source = ZigBee(serial.Serial(source,baud), callback=self._gotFrame)
                        else: source = ZigBee(serial.Serial(source,baud))
                    except serial.SerialException:
                        print "WARNING: Could not open the provided ZigBee's source serial port (%s)" % source
                else:
                    print "ERROR: linkType was corrupted while searching for OS-dependent COM markers. This is really strange."
                return source
            else:
                print 'ERROR: Invalid COM port passed'
            
        #HTTP
        elif (self.linkType == 'http'):
            foundURL = re.findall(r'(https?://\S+)', source)
            if (len(foundURL)==1):
                source = httplib.HTTPConnection(source)
                return source
            else:
                print 'ERROR: Invalid URL passed. Make sure the http:// portion of the url is present. Do not input more than one url.'

        #Not one of the accepted types
        else:
            print 'ERROR: Invalid linkType string. Accepted values are: %s' % allSources

    def _testSource(self, source):
        """
        Test that the device attached to the [source] COM port is responsive. If not, try to identify the error source.
        Acceptable: 
        """
        pass
        #XBee
        if (source.__class__ == XBee):
            #NEED TO TEST IN VIVO!
            try:
                timedTest = TimeLimited(self._testBee, 2)
                response = timedTest()
                comments = response
                success = 1
            except TimeLimitExpired:
                try:
                    timedTest = TimeLimited(self._testXBeeAPI, 2)
                    response = timedTest()
                    comments = 'The XBee on port %s seems to be in API mode (ATAP=%s) but did not respond to the initial test. \n\
                    This is strange behaviour, perhaps it failed on the first message. \
                    Try testing twice in a row in your program :)' % (source.serial.port, response['parameters'])
                    success = 0
                except TimeLimitExpired:
                    comments = 'The XBee on port %s seems to be in AT mode (transparent mode, where ATAP=0). \n \
                    You need to put the XBee in API mode (ATAP=1 or 2).' % source.serial.port
                    success = 0
    
        #ZigBee
        elif (source.__class__ == ZigBee):
            try:
                timedTest = TimeLimited(self._testBee, 2)
                response = timedTest()
                comments = response
                success = 1
            except TimeLimitExpired:
                comments = 'No response received from device on port %s \n Ensure that your ZigBee \
                has been flashed with an API firmware' % source.serial.port
                success = 0
        #HTTP
        elif (source.__class__ == httplib.HTTPConnection):
            #NOT FULLY IMPLEMENTED, TEST FOR EXISTENCE OF HEADERS OR PREDETERMINED SCRIPT ON SERVER
            source.request("GET","/index.php")
            response = source.getresponse()
            if(response.status == 404):
                success = 0
                comments = response.status, response.reason
            else:
                success = 1
                comments = ""
        else:
            comments = 'Error: Unexpected source class - ', source.__class__
    
        return success,comments
    
    def _testBee(self, source):
        """
        Sends the ATVR command through API mode to the [source] bee object. Necessary in callable type for timeout code
        Return the response packet
        Acceptable (as xbee package objects, see python-xbee or pyXBee for object definition):
            xbee.XBee()
            xbee.ZigBee()
        """
        pass
        source.send('at',command='vr')
        return source.wait_read_frame()
    
    def _testXBeeAPI(self):
        """
        Check whether the XBee is in API mode (ATAP=1 or 2). If not in API mode (ATAP=0), the command will timeout. Necessary in callable type for timeout code
        Return the response packet
        Acceptable (as xbee package object, see python-xbee or pyXBee for object definition):
            xbee.XBee()
        """
        #IN FUTURE THIS SHOULD BE INCLUDED IN THE MODIFIED XBEE LIBRARY
        pass
        source.send('at',command='ap')
        return source.wait_read_frame()