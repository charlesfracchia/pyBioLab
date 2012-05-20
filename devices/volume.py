"""
volume.py

by Charles Fracchia, 2012

Volume class module

This class defines data and methods common to all Volume dispenser devices.
"""

class Volume(object):
    """docstring for Volume"""
    
    def setVolume(self,volume):
        """Sets the [volume] for the volume dispenser"""
        pass
    
    def dispense(self,rcf):
        """Sets the [rcf] for the shaker"""
        pass
    
    def __init__(self, maxSpeed):
        super(Volume, self).__init__()
        self.minVolume = minVolume
        self.maxVolume = maxVolume
        

#Testing
#m = Shaker(300)
#print m.maxSpeed
#print m.maxTemp
        
        