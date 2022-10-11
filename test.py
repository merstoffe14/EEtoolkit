from electronicsToolkit import EEToolkit
from eecomplex import EEComplex

eet = EEToolkit()

z1 = EEComplex.fromPolar(100,0,"Ohm")
z2 = EEComplex.fromPolar(50,0,"Ohm")
z3 = EEComplex.fromPolar(25,0,"Ohm")

v1 = EEComplex.fromPolar(230,0,"V")
v2 = EEComplex.fromPolar(230,0,"V")

print(eet.parallelImpedance([z1,z2,z3]))

eet.drawPhasor(v1)








