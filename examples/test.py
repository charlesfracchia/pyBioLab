from pybiolab.devices.newbrunswick.innova_44_44R import Innova_44_44R

dodo = Innova_44_44R()
print dodo.maxSpeed
print dodo.minTemp
print dodo.maxTemp
dodo.setRPM("200")
