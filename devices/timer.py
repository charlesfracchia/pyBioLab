"""
timer.py

by Charles Fracchia, 2012

Timer class module

This class defines data and methods common to all timers.
"""

class Electricity(object):
    """docstring for Timers"""
    
    def start(self):
        """Starts the timer"""
        pass
    
    def pause(self):
        """Pauses the timer"""
        pass
    
    def stop(self):
        """Stops the timer"""
        pass    
    
    def __init__(self, maxSpeed):
        super(Timer, self).__init__()
        self.maxTime = maxTime
        

#Testing
#m = Shaker(300)
#print m.maxSpeed
#print m.maxTemp
        
        