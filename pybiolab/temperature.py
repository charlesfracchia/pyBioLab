"""
temperature.py

by Charles Fracchia, 2012

Temperature class module

This class defines data and methods common to all Temperature managers.
"""

class Temperature(object):
    """docstring for Shaker"""
    
    def setTemp(self,temp):
        """Sets the [temp] for the temperature manager"""
        pass
    
    def __init__(self, minTemp, maxTemp):
        super(Temperature, self).__init__()
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        

#Testing
#m = Shaker(300)
#print m.maxSpeed
#print m.maxTemp
        
        