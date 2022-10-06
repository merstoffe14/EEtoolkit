import math
from math import radians, degrees

class Phasor:

    #In physics and engineering, a phasor (a portmanteau of phase vector)
    #is a complex number representing a sinusoidal function whose
    #amplitude (A), angular frequency (ω), and initial phase (θ) are time-invariant.

    #Impedance values can also be saved in the form of phasors, altough they do not have an angular frequency
    #Admitances as well, if no frequency is given, the program will asume it is an impedance
    #If it has to be an admitance, you can leave out the frequency but will need to give the correct unit S
    # I might remove this, to avoid confusion, and will make the unit argument not optional.

    def __init__(self, magnitude, argument, realComponent, imaginaryComponent, frequency=None, unit=None) -> None:

        if frequency == None:
            if unit == None or unit == "Ohm":  
                self.unit = "Ohm"
                self.isZY = [True, "Impedance"]
            if unit == "S":
                self.unit = "S"
                self.isZY = [True, "Admitance"]
            self.angularFrequency = None
            self.period = None
        else:   
            self.isZY = [False, None] 
            self.unit = unit
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
        return cls(magnitude, argument, realComponent, imaginaryComponent, frequency, unit)

    @classmethod
    def fromPolar(cls, magnitude: float, argument: float, unit: str = None, frequency: float = None):
        realComponent = math.cos(radians(argument))*magnitude
        imaginaryComponent = math.sin(radians(argument))*magnitude
        return cls(magnitude, argument, realComponent, imaginaryComponent, frequency, unit)
      

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
