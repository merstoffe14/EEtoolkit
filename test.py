from electronicsToolkit import EEToolkit
from phasor import Phasor

eet = EEToolkit()

v1 = Phasor.fromComplex(30, 10, "V", 50)
i1 = Phasor.fromPolar(25,45, "A", 50)
z1 = Phasor.fromComplex(30, 20)

print(v1.printString("complex"))
print(v1.printString("polar"))

print(i1.printString("complex"))
print(i1.printString("polar"))
