import math
from math import radians, degrees

class Phasor:

    #In physics and engineering, a phasor (a portmanteau of phase vector)
    #is a complex number representing a sinusoidal function whose
    #amplitude (A), angular frequency (ω), and initial phase (θ) are time-invariant.

    #Impedance values can also be saved in the form of phasors, altough they do not have an angular frequency
    #Admitances as well

    def __init__(self, magnitude, argument, realComponent, imaginaryComponent, unit, frequency=None) -> None:

        if frequency == None:
            if unit == "Ohm":
                self.unit = "Ohm"
                self.isZY = [True, "Impedance"]
                self.frequency = None
                self.angularFrequency = None
                self.period = None

            if unit == "S":
                self.unit = "S"
                self.isZY = [True, "Admitance"]
                self.frequency = None
                self.angularFrequency = None
                self.period = None
        
            else:   
                self.unit = unit
                self.isZY = [False, None] 
                self.frequency = None
                self.angularFrequency = None
                self.period = None
        else:
            self.unit = unit
            self.isZY = [False, None]
            self.angularFrequency = frequency*math.pi*2
            self.period = 1/frequency
            self.frequency = frequency

        self.magnitude = magnitude
        self.argument = argument
        self.realComponent = realComponent
        self.imaginaryComponent = imaginaryComponent
        self.complexNotation = [self.realComponent, self.imaginaryComponent]

        # UNIT DETECTION, This can be done better, by making units an actual thing instead of strings
        # U = ZI
        if self.unit == "(Ohm)*(A)" or self.unit == "(A)*(Ohm)" or self.unit == "(A)/(S)" :
            self.unit = "V"
        # I = U/Z
        if self.unit == "(V)/(Ohm)" or self.unit == "(V)*(S)":
            self.unit = "A"
        # Z = U/I
        if self.unit == "(V)/(A)":
            self.unit = "Ohm"
        # Y = I/U
        if self.unit == "(A)/(V)":
            self.unit = "S"
    




    @classmethod
    def fromComplex(cls, realComponent: float, imaginaryComponent: float, unit: str = None, frequency: float = None):   
        magnitude = math.sqrt(realComponent**2 + imaginaryComponent**2)
        argument = degrees(math.atan(imaginaryComponent/realComponent))
        return cls(magnitude, argument, realComponent, imaginaryComponent, unit, frequency)

    @classmethod
    def fromPolar(cls, magnitude: float, argument: float, unit: str = None, frequency: float = None):
        realComponent = math.cos(radians(argument))*magnitude
        imaginaryComponent = math.sin(radians(argument))*magnitude
        return cls(magnitude, argument, realComponent, imaginaryComponent, unit, frequency)
      

    def printString(self, notation):

        if notation == "complex":
            if self.imaginaryComponent < 0:
                string = f"{round(self.realComponent,2)} - j{round(abs(self.imaginaryComponent), 2)} {self.unit}"
            else:
                string = f"{round(self.realComponent, 2)} + j{round(abs(self.imaginaryComponent), 2)} {self.unit}"
            return string

        if notation == "polar":
            string = f"{round(self.magnitude, 2)}∠{round(self.argument, 2)}° {self.unit}"
            return string
        else:
            return "notation unknown"


     # FUNDAMENTAL OPERATIONS ------------------------------------

    def __add__(self, p2):

        unit = self.unit
        frequency = self.frequency

        if not (self.unit == p2.unit or self.frequency == p2.frequency):
            print("Phasors should have the same unit and frequency!")
            return
        real = self.realComponent + p2.realComponent
        imaginary = self.imaginaryComponent + p2.imaginaryComponent
        return Phasor.fromComplex(real, imaginary, unit, frequency)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return other.__add__(self)

    def __sub__(self, p2):

        unit = self.unit
        frequency = self.frequency

        if not (self.unit == p2.unit or self.frequency == p2.frequency):
            print("Phasors should have the same unit and frequency!")
            return
        real = self.realComponent - p2.realComponent
        imaginary = self.imaginaryComponent - p2.imaginaryComponent
        return Phasor.fromComplex(real, imaginary, unit, frequency)
    
    def __mul__(self, p2):

        #MULTIPLYING TWO PHASORS WITH DIFFERENT FREQUENCY
        # if you are trying to multiply with an impedance, it ignores the frequency check
        if not self.frequency == p2.frequency and not (self.isZY[0] or p2.isZY[0]):
            print("You can't multiply 2 phasors with different frequencies")
            return
        #It sets the frequency of the new phasor to the frequency of the not-impedance value
        if self.isZY[0]:
            frequency = p2.frequency
        else:
            frequency = self.frequency

        argument = self.argument + p2.argument
        magnitude = self.magnitude * p2.magnitude

        unit = f"({self.unit})*({p2.unit})"

        p12 = Phasor.fromPolar(magnitude, argument, unit, frequency)
        return p12
        

    def __truediv__(self, p2):
        #MULTIPLYING TWO PHASORS WITH DIFFERENT FREQUENCY
        # if you are trying to multiply with an impedance, it ignores the frequency check
        if not self.frequency == p2.frequency and not (self.isZY[0] or p2.isZY[0]):
            print("You can't multiply 2 phasors with different frequencies")
            return
        #It sets the frequency of the new phasor to the frequency of the not-impedance value
        if self.isZY[0]:
            frequency = p2.frequency
        else:
            frequency = self.frequency

        argument = self.argument - p2.argument
        magnitude = self.magnitude / p2.magnitude

        unit = f"({self.unit})/({p2.unit})"

        p12 = Phasor.fromPolar(magnitude, argument, unit, frequency)
        return p12

    def getAdmitanceFromZ(self, p1):
        magnitude = 1/(p1.magnitude)
        argument = -p1.argument
        return Phasor.fromPolar(magnitude, argument, "S")

    def getImpedanceFromY(self, p1):
        magnitude = 1/(p1.magnitude)
        argument = -p1.argument
        return Phasor.fromPolar(magnitude, argument, "Ohm")
