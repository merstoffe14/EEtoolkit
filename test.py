from electronicsToolkit import EEToolkit
from phasor import Phasor

eet = EEToolkit()

v1 = Phasor.fromComplex(230, 0, "V", 50)

z1 = Phasor.fromComplex(100, 0)

i1 = eet.ohmsLaw(v1,z1)
v2 = eet.ohmsLaw(z1,i1)
print(i1.printString("polar"))
print(v2.printString("polar"))

