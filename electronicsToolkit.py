import math
from math import radians
from mimetypes import init

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
        

    def addPhasor(self, p1: Phasor, p2: Phasor):
        
        real = p1.realComponent + p2.realComponent
        imaginary = p1.imaginaryComponent + p2.imaginaryComponent
        p12 = Phasor("_","_", real, imaginary)
        return p12
    

    #Is er een betere manier voor deze optional argumetns
    def subtractPhasor(self, p1: Phasor, p2: Phasor):
        
        real = p1.realComponent - p2.realComponent
        imaginary = p1.imaginaryComponent - p2.imaginaryComponent
        p12 = Phasor("_","_", real, imaginary)
        return p12

    def multiplyPhasor(self, p1: Phasor, p2: Phasor):
        
        argument = p1.argument * p2.argument
        magnitude = p1.magnitude + p2.magnitude
        p12 = Phasor(magnitude, argument)
        return p12

    def dividePhasor(self, p1: Phasor, p2: Phasor):

        argument = p1.argument / p2.argument
        magnitude = p1.magnitude - p2.magnitude
        p12 = Phasor(magnitude, argument)
        return p12

    def activePower(self):
        pass

    def reactivePower(self):
        pass

    def apparentPower(self):
        pass

    def calculateImpedance(self, R, L ,C , omega):
        pass

    


