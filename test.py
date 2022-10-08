from cmath import phase
from electronicsToolkit import EEToolkit
from phasor import Phasor

eet = EEToolkit()

r1 = Phasor.fromComplex(100, 0, "Ohm")
r2 = Phasor.fromComplex(101, 0, "Ohm")
r3 = Phasor.fromComplex(100, 0, "Ohm")

v1 = Phasor.fromComplex(230, 0, "V")
i1 = Phasor.fromComplex(2, 0, "A")

ohmcheck = eet.ohmsLaw(v1, r1)
print(ohmcheck.printString("polar"))

print(eet.parallel([r1,r2,r3]).printString("polar"))

rs = [r1,r2,r3]

rt = r1 / r2

# Sum werkt nog ni door radd
r4 = sum(rs)

print(rt.printString("polar"))

r_t = eet.parallel([r2,r1, r3])
print(r_t.printString("polar"))





