"""
syringe.py

by Charles Fracchia, Copyright (c) 2012

Syringe Pump class module

This class defines data and methods common to all Syringe pumps.
"""

class SyringePump(object):
    """docstring for Syringe Pump"""
    
    def __init__(self, minDiameter, maxDiameter):
        self.minDiameter = minDiameter
        self.maxDiameter = maxDiameter