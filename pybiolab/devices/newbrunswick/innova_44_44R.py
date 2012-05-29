from pybiolab import Shaker
from pybiolab import Temperature

class Innova_44_44R(Shaker,Temperature):
    """docstring for Innova_44_44R"""
    def __init__(self):
        #super(Innova_44_44R, self).__init__()
        self.maxSpeed = 300
        self.minTemp = 4
        self.maxTemp = 80
    
    def setRPM(self,rpm):
        """Sets the [rpm] for the shaker"""
        pass
        
