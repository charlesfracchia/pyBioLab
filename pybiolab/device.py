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
import inspect

allBaud = [300,1200,2400,4800,9600,14400,19200,28800,38400,57600,115200,230400]
#Types of supported connections
allSources = ['xbee','zigbee','http']

class Device(object):
    """docstring for Device"""
    
    def __init__(self, dId, brand, model, modelNo, source, destination, linkType, echo=True, baud=9600, synchronous=True):
        self.id = dId
        self.brand = brand
        self.model = model
        self.modelNo = modelNo
        self.synchronous = synchronous
        self.linkType = self._checkLink(linkType)
        self.destination = self._checkDestination(destination)
        self.baud = self._checkBaud(baud)
        self.source = self._checkSource(source, baud, synchronous)
        self.commandTerminator = '\r'
        self.pendingResponses = []
    
    #Send
    def sendCommand(self,command,**kwargs):
        """
        Send the [command] passed after checking that it is in [self.commands] (the command list) for the device
        Return the raw response (in future automatically parse the response)
        cmd,**kwargs -> _parseCommand() -> _send()
        """
        pass
        if(command not in self.commands):
            raise ValueError, 'The command you are trying to send (%s) was not found in the list of commands defined for this device (%s/%s)' % (command,self.brand,self.model)
        else:
            expectedArgs = self.commands[command].count('!')/2
            if(expectedArgs != 0 and expectedArgs != len(kwargs)): raise ValueError, 'Expecting arguments but none were passed.'
            parsedCommand = self._parseCommand(self.commands[command],**kwargs)
            self._send(parsedCommand)
            #add sent command to the sentCommand array
            self.pendingResponses.append(self.commands[command])
    
    def _parseCommand(self, command, **kwargs):
        """
        Parse command by replacing all arguments in the command
        """
        pass
        
        #For each argument in function, replace the variable with the passed value
        for argKey in kwargs:
            #print "Replacing argument: ",argKey       #DEBUG
            #Make the string to replace, strings are immutable in python use list of chars
            #arg -> !arg!
            listArg = list(argKey)
            listArg.insert(0,"!")
            listArg.insert(len(listArg),"!")
            argString = "".join(listArg)
            #print "Arg String: ",argString     #DEBUG
            #print "kwarg", kwargs[argKey]   #DEBUG
            #Strip the variable and replace with value passed to the device type layer function (eg: setRPM)
            command = command.replace(argString,str(kwargs[argKey]))
            #print command     #DEBUG
            
        #Check that no arguments have been left unreplaced (!arg!)
        if (command.find('!') == -1):
            #Append the command terminator at the end
            listCommand = list(command)
            listCommand.insert(len(listCommand),self.commandTerminator)
            command = "".join(listCommand)
            return command
        else:
            raise ValueError, 'Some arguments have not been replaced with their values. You likely forgot to pass the argument when calling device command or have not defined your device type layer function (eg: setRPM() in shaker.py) correctly.'
    
    def _send(self,command):
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
         print 'Sent!'
         
         if (self.synchronous==True):
            response = self.source.wait_read_frame()
            return response
         else:
            return None
    
    #Response Parsing
    def parseResponse(self,response):
        """
        
        """
        pass
        matchedCommands = 0
        matchedFormat = None
        #Search through sent commands
        
        for index,pendingResponse in enumerate(self.pendingResponses):
            #Check whether one of the recently sent commands has a response format defined
            #print 'Checking match for ', pendingResponse       DEBUG
            matches = self._checkFormat(response['rf_data'],pendingResponse)
            if matches: 
                matchedCommands += 1
                matchedFormat = pendingResponse
        if(matchedCommands>1):
            print 'WARNING: your response matches could be responses to more than one of the commands sent to the device recently.'
        elif(matchedCommands==0):
            #print 'Was not found in sent commands. Searching through all defined responses'        DEBUG
            for deviceResponse in self.responses:
                #print 'Checking ',deviceResponse       DEBUG
                matches = self._checkFormat(response['rf_data'],self.responses[deviceResponse])
                if matches: 
                    matchedCommands += 1
                    matchedFormat = self.responses[deviceResponse]
                    print matchedFormat
            if(matchedCommands>1):
                print 'WARNING: your response matches could be responses to more than one of the commands sent to the device recently.'
            elif(matchedCommands==0):
                print 'WARNING: the response data received does not match any defined format. You are likely not incorporating enough responses in the [self.responses] dictionnary of your device definition. The response received in this case is: %s' % response['rf_data']
                #raise ValueError, 'No command you have sent '
        else:
            #parse the variables 
            parsedVariables = self._parseVariables(response['rf_data'],matchedFormat)
            
            #print 'Matched:',matchedFormat     DEBUG
        
        #Additional check if the device is allowed to just spew data un
        #Or if one command generates many more packet answers
    
    def _parseVariables(self,responseData,format):
        """
        Returns a dictionnary of the variableName:value
        """
        pass
        variableNames = self._getVariables(format,False)
        print variableNames
        for variable in variableNames:
            print 'variable: ', variable
            format = format.replace(variable,'((?:[a-zA-Z0-9_]*))')
            print 'format: ', format
        variableValues = re.compile(format).findall(responseData)
        
        varVal = {}
        for index,variableName in enumerate(variableNames):
            varVal[variableName.replace('!','')] = variableValues[index]
        return varVal
        
    def _checkFormat(self,packetData,responseFormat):
        """
        Check whether the [packetData] matches the expected [responseFormat]
        Acceptable:
            packetData = 'rf_data' field of response packet type 'rx'
            responseFormat = [self.responses] string
        """
        pass
        #build the custom regex from the responseFormat
        variables = self._getVariables(responseFormat)
        #replace the variables (!variableName!)
        for variable in variables:
            responseFormat = responseFormat.replace(variable,'((:?[a-zA-Z0-9_]*))')
        #escape the special characters that can be found in commands
        for specialChar in ['\t','\r']:
            charList = list(specialChar)
            responseFormat = responseFormat.replace(specialChar,'+\\%s' % charList[-1])
            
        #print 'Format is:', responseFormat
        found = re.compile(responseFormat).search(packetData)
        if(found!=None):
            return True
        else:
            print False
    
    def _getVariables(self,deviceResponseString,stripped=False):
        """
        Returns the variables from a [self.response] string
        """
        pass
        variableRegex='(!(?:[a-zA-Z0-9_]*)!)'
        variables = re.compile(variableRegex).findall(deviceResponseString)
        if stripped:
            for index,variable in enumerate(variables):
                variables[index] = variables[index].replace('!','')
        return variables
    
    def _gotFrame(self,data):
        """
        Parse the received packed. This function is called asynchronously when the device.source (xbee or zigbee) receives a packet
        Return the received packet
        Acceptable:
            XBee.response object
        """
        pass
        try:
            if data['id']=='tx_status':
                if data['deliver_status']=='\x25': print 'Packet Error: Route Not Found'
                
            elif data['id']=='at_response':
                print ''
                #print "\t\t%s\t(%s)" % (data['parameter']['node_identifier'],data['parameter']['source_addr_long'].encode('hex'))
            elif data['id']=='rx':
                self.parseResponse(data)
            else:
                print data
        except KeyError:
            print 'Error: Uninplemented response packet type'
    
    #Checks
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
    