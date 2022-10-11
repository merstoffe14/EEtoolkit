from cmath import phase
from queue import Empty
from tracemalloc import start
from electronicsToolkit import EEToolkit
from eecomplex import EEComplex

eet = EEToolkit()

z1 = EEComplex.fromPolar(100,0,"Ohm")
v1 = EEComplex.fromPolar(230,0,"V")

i1 = v1/z1

y1 = eet.getAdmitanceFromZ(z1)


print(i1)
print(y1)


# check if number is prime 






