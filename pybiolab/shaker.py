"""
shaker.py

by Charles Fracchia, Copyright (c) 2012

Shaker class module

This class defines data and methods common to all Shaker devices.
"""

class Shaker(object):
    """docstring for Shaker"""
    
    def __init__(self, maxSpeed):
        self.maxSpeed = maxSpeed
    
    def setRPM(self,rpm):
        """Sets the [rpm] for the shaker"""
        pass
    
    def setRCF(self,rcf):
        """Sets the [rcf] for the shaker"""
        pass
        