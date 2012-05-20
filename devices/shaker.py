"""
shaker.py

by Charles Fracchia, 2012

Shaker class module

This class defines data and methods common to all Shaker devices.
"""

class Shaker(object):
    """docstring for Shaker"""
    
    def setRPM(self,rpm):
        """Sets the [rpm] for the shaker"""
        pass
    
    def setRCF(self,rcf):
        """Sets the [rcf] for the shaker"""
        pass
    
    def __init__(self, maxSpeed):
        super(Shaker, self).__init__()
        self.maxSpeed = maxSpeed
        

#Testing
#m = Shaker(300)
#print m.maxSpeed
#print m.maxTemp
        
        