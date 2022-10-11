from electronicsToolkit import EEToolkit
from eecomplex import EEComplex

eet = EEToolkit()

z_rlc = eet.calculateImpedance(R = 10, L = 0.1, C = 0.0001, frequency = 50)
print(z_rlc)
z1 = EEComplex.fromPolar(100,0,"Ohm")
z2 = EEComplex.fromPolar(50,0,"Ohm")
z3 = EEComplex.fromPolar(25,0,"Ohm")

v1 = EEComplex.fromPolar(230,0,"V", 50)
v2 = EEComplex.fromComplex(230,100,"V", 50)

print(eet.parallelImpedance([z1,z2,z3]))

eet.drawScopeView([v1,v2])







