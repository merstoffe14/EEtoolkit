import math
from math import radians, degrees

class EEComplex:

    # In physics and engineering, a phasor (a portmanteau of phase vector)
    # is a complex number representing a sinusoidal function whose
    # amplitude (A), angular frequency (ω), and initial phase (θ) are time-invariant.

    # Impedance values can also be saved in the form of phasors, altough they do not have an angular frequency
    # Admitances as well

    # To capture all of these in 1 simple object, we use the EEComplex.
    # It is recomended to define a "Global" frequency variable, and set it at the top of your worksheet.


    def __init__(self, complexNumber: complex, units: list[list[str],list[str]], frequency: float = None) -> None:
        
        self.units = units
        self.complex = complexNumber
        self.frequency = frequency

        self.eecomplexChecker()
        self.unitChecker()



    # When using the classmethods, you should just give a string for unit, this unit will end up in the nominator
    @classmethod
    def fromComplex(cls, realComponent: float, imaginaryComponent: float, unit: str, frequency: float = None):   
        complexNumber = complex(realComponent, imaginaryComponent)

        # Check if the unit given is a singular or plural
        if isinstance(unit, str):
            units = [[unit], []]
        else:
            units = unit

        return cls(complexNumber, units, frequency)

    @classmethod
    def fromPolar(cls, magnitude: float, argument: float, unit: str, frequency: float = None):
        realComponent = math.cos(radians(argument))*magnitude
        imaginaryComponent = math.sin(radians(argument))*magnitude
        complexNumber = complex(realComponent, imaginaryComponent)

        # Check if the unit given is a singular or plural
        if isinstance(unit, str):
            units = [[unit], []]
        else:
            units = unit

        return cls(complexNumber, units, frequency)

    # Check if it has a frequency, if so unit can only be V or A
    def eecomplexChecker(self):
        
        for i in self.units[0]:
            if i not in ["V", "A", "Ohm", "S"]:
                raise ValueError("Nominator must only contain be V, A, S or Ohm")
        for i in self.units[1]:
            if i not in ["V", "A", "Ohm", "S"]:
                raise ValueError("Denominator must only contain V, A, S or Ohm")


    # I really want a better way to do this, but I can't think of one right now.
    def unitChecker(self):
        nominator = self.units[0]
        denominator = self.units[1]

        #Remove the common units from the nominator and denominator
        commonUnits = [value for value in nominator if value in denominator]
        for unit in commonUnits:
            nominator.remove(unit)
            denominator.remove(unit)

        #Check if combination of units is another unit
        # U = ZI, I = U/Z, Z = U/I
        if "Ohm" in nominator and "A" in nominator:
            nominator.remove("Ohm")
            nominator.remove("A")
            nominator.append("V")
        if "V" in nominator and "Ohm" in denominator:
            nominator.remove("V")
            denominator.remove("Ohm")
            nominator.append("A")
        if "V" in nominator and "A" in denominator:
            nominator.remove("V")
            denominator.remove("A")
            nominator.append("Ohm")
        # V = A/S, A = V/S, S = V/A
        # Might add more later

        
    def getRealComponent(self):
        return self.complex.real  

    def getImaginaryComponent(self):
        return self.complex.imag

    def getMagnitude(self):
        return abs(self.complex)

    def getArgument(self):
        return degrees(math.atan(self.getImaginaryComponent()/self.getRealComponent()))

    def __str__(self):
        nominatorString = ""
        denominatorString = ""
        for i in self.units[0]:
            nominatorString += str(i)       
        for i in self.units[1]:
            denominatorString += str(i)
            
        if denominatorString == "":
            unitsstring = nominatorString
        elif nominatorString == "":
            unitsstring =  "1/" + denominatorString
        else:
            unitsstring = nominatorString + "/" + denominatorString
        

        return f"{self.getRealComponent()} + j{self.getImaginaryComponent()} {unitsstring} | {self.getMagnitude()}∠{self.getArgument()}° {unitsstring}"

    def __add__(self, other: "EEComplex") -> "EEComplex":

        if self.frequency != other.frequency:
            return ValueError("Frequencies must be the same!")
        if self.units != other.units:
            return ValueError("Units must be the same!")

        real = self.getRealComponent() + other.getRealComponent()
        imaginary = self.getImaginaryComponent() + other.getImaginaryComponent()
        
        return EEComplex.fromComplex(real, imaginary, self.units, self.frequency)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return other.__add__(self)

    def __sub__(self, other: "EEComplex") -> "EEComplex":
        
        if self.frequency != other.frequency:
            return ValueError("Frequencies must be the same!")
        if self.units != other.units:
            return ValueError("Units must be the same!")

        real = self.getRealComponent() - other.getRealComponent()
        imaginary = self.getImaginaryComponent() - other.getImaginaryComponent()
        
        return EEComplex.fromComplex(real, imaginary, self.units, self.frequency)
    
    def __mul__(self, other: "EEComplex") -> "EEComplex":

        #MULTIPLYING TWO PHASORS WITH DIFFERENT FREQUENCY is not allowed
        # if you are trying to multiply with an impedance, it ignores the frequency check
        if (self.frequency != other.frequency) and (other.frequency != None or self.frequency != None):
            return ValueError("Frequencies must be the same!")
        #It sets the frequency of the new phasor to the frequency of the not-impedance value
        if self.frequency == None:
            frequency = other.frequency
        else:
            frequency = self.frequency
        
        argument = self.getArgument() + other.getArgument()
        magnitude = self.getMagnitude() * other.getMagnitude()

        nominator = self.units[0] + other.units[0]
        denominator = self.units[1] + other.units[1]
        units = [[nominator], [denominator]]
        
        return EEComplex.fromPolar(magnitude, argument, units, frequency)
        

    def __truediv__(self, other: "EEComplex") -> "EEComplex":

        #DIVIDING TWO PHASORS WITH DIFFERENT FREQUENCY is not allowed
        # if you are trying to multiply with an impedance, it ignores the frequency check
        if (self.frequency != other.frequency) and (other.frequency != None or self.frequency != None):
            return ValueError("Frequencies must be the same!")
        #It sets the frequency of the new phasor to the frequency of the not-impedance value
        if self.frequency == None:
            frequency = other.frequency
        else:
            frequency = self.frequency
        
        argument = self.getArgument() - other.getArgument()
        magnitude = self.getMagnitude() / other.getMagnitude()

        nominator = self.units[0] + other.units[1]
        denominator = self.units[1] + other.units[0]
        units = [nominator, denominator]
        
        return EEComplex.fromPolar(magnitude, argument, units, frequency)

