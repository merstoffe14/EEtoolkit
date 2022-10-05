from electronicsToolkit import EEToolkit
from phasor import Phasor

eet = EEToolkit()

v1 = Phasor.fromComplex(230, 0, "V", 50)

z1 = Phasor.fromComplex(100, 0)

i1 = eet.dividePhasor(v1,z1)
print(i1.printString("polar"))

