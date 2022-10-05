import math
from math import radians
from mimetypes import init
from typing import Optional

from phasor import Phasor


class EEToolkit:

    import numpy as np
    from phasor import Phasor


    # I am not sure if you would use RMS or PEAK value for phasors, I need to check my handbook
    # In my head it would be PEAK value because then the phasor will draw the correct sinusoidal wave
    # But if I remember correctly we always use RMS
    # If we calculate a power, we use phasors using RMS (logical because for ac power calculations you need to use RMS)
    def __init__(self) -> None:

        self.standardValues = {
            "mains_us": Phasor.fromComplex(120, 0, "V", 60),
            "mains": Phasor.fromComplex(230, 0, "V", 50),
        }
        
    def addPhasor(self, p1: Phasor, p2: Phasor) -> Optional[Phasor]:

        if not p1.unit == p2.unit:
            print("You can't add phasors with 2 different units!")  
            return 
        if not p1.frequency == p2.frequency:
            print("You can't add 2 phasors with different frequencies")
            return

        real = p1.realComponent + p2.realComponent
        imaginary = p1.imaginaryComponent + p2.imaginaryComponent
        p12 = Phasor.fromComplex(real, imaginary, p1.unit, p1.frequency)
        return p12
    

    def subtractPhasor(self, p1: Phasor, p2: Phasor) -> Optional[Phasor]:
        
        if not p1.unit == p2.unit:
            print("You can't subtract phasors with 2 different units!")
            return
        if not p1.frequency == p2.frequency:
            print("You can't add 2 phasors with different frequencies")

        real = p1.realComponent - p2.realComponent
        imaginary = p1.imaginaryComponent - p2.imaginaryComponent
        p12 = Phasor.fromComplex(real, imaginary, p1.unit, p1.frequency)
        return p12

    def multiplyPhasor(self, p1: Phasor, p2: Phasor) -> Optional[Phasor]:
        
        #MULTIPLYING TWO PHASORS WITH DIFFERENT FREQUENCY
        if not p1.frequency == p2.frequency and not (p1.isImpedance or p2.isImpedance):
            print("You can't multiply 2 phasors with different frequencies")
            return
        if p1.isImpedance:  frequency = p2.frequency
        else:   frequency = p1.frequency

        argument = p1.argument + p2.argument
        magnitude = p1.magnitude * p2.magnitude

        unit = f"({p1.unit})*({p2.unit})"    

        p12 = Phasor.fromPolar(magnitude, argument, unit, frequency)
        return p12

    def dividePhasor(self, p1: Phasor, p2: Phasor) -> Optional[Phasor]:

        #DIVIDING TWO PHASORS WITH DIFFERENT FREQUENCY
        if not p1.frequency == p2.frequency and not (p1.isImpedance or p2.isImpedance):
            print("You can't divide 2 phasors with different frequencies")
            return
        if p1.isImpedance:  frequency = p2.frequency
        else:   frequency = p1.frequency

        argument = p1.argument - p2.argument
        magnitude = p1.magnitude / p2.magnitude
        if p1.unit == p2.unit:
            unit = "ul"
        else:
            unit = f"({p1.unit})/({p2.unit})"

        p12 = Phasor.fromPolar(magnitude, argument, unit, frequency)
        return p12

    def ohmsLaw(self, p1, p2):

        phasors = {
            p1.unit: p1,
            p2.unit: p2,
        }

        # U = ZI
        if ("Ohm" in phasors) and ("A" in phasors):
            return self.multiplyPhasor(p1,p2)
        # I = U/Z
        if ("V" in phasors) and ("Ohm" in phasors):  
            return self.dividePhasor(phasors["V"], phasors["Ohm"])
        # Z = U/I
        if ("V" in phasors) and ("A" in phasors):
            return self.dividePhasor(phasors["V"] , phasors["A"])

    def activePower(self):
        pass

    def reactivePower(self):
        pass

    def apparentPower(self):
        pass

    def calculateImpedance(self, R, L ,C , omega):
        pass

    


