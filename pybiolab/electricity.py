"""
electricity.py

by Charles Fracchia, Copyright (c) 2012

Electricity class module

This class defines data and methods common to all electric power supplies.
"""

class Electricity(object):
    """docstring for Electricity manager"""
    
    def setVoltage(self,voltage):
        """Sets the output [voltage] for the power supply"""
        pass
    
    def setCurrent(self,current):
        """Sets the output [current] for the power supply"""
        pass
    
    def __init__(self, maxSpeed):
        super(Electricity, self).__init__()
        self.maxVoltage = maxVoltage
        self.maxCurrent = maxCurrent
        

#Testing
#m = Shaker(300)
#print m.maxSpeed
#print m.maxTemp
        
        