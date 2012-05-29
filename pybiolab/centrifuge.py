"""
centrifuge.py

by Charles Fracchia, 2012

Centrifuge class module

This class defines data and methods common to all Centrifuges.
"""

class Centrifuge(object):
    """docstring for centrifuge"""
    
    def setRPM(self,rpm):
        """Sets the [rpm] for the centrifuge"""
        pass
    
    def setRCF(self,rcf):
        """Sets the [rcf] for the centrifuge"""
        pass
    
    def __init__(self, maxSpeed):
        super(Centrifuge, self).__init__()
        self.maxSpeed = maxSpeed