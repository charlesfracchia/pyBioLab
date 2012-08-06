"""
temperature.py

by Charles Fracchia, Copyright (c) 2012

Temperature class module

This class defines data and methods common to all Temperature managers.
"""

class Temperature(object):
    """docstring for Shaker"""
    
    def __init__(self, minTemp, maxTemp):
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        
    def setTemp(self,temp):
        """Sets the [temp] for the temperature manager"""
        pass