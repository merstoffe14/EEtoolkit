import math
from math import radians
from mimetypes import init
from typing import Optional

from phasor import Phasor


class EEToolkit:

    import numpy as np
    from phasor import Phasor
    import matplotlib.pyplot as plt


    # I am not sure if you would use RMS or PEAK value for phasors, I need to check my handbook
    # In my head it would be PEAK value because then the phasor will draw the correct sinusoidal wave
    # But if I remember correctly we always use RMS
    # If we calculate a power, we use phasors using RMS (logical because for ac power calculations you need to use RMS)
    def __init__(self) -> None:

        self.standardValues = {
            "mains_us": Phasor.fromComplex(120, 0, "V", 60),
            "mains": Phasor.fromComplex(230, 0, "V", 50),
        } 

    def ohmsLaw(self, p1, p2) -> Phasor:

        # I can avoid using this dict by calling the function with ohmsLaw(x = .., y = ..) and  then working with default values.
        phasors = {
            p1.unit: p1,
            p2.unit: p2,
        }

        # U = ZI
        if ("Ohm" in phasors) and ("A" in phasors):
            return p1 * p2
        # I = U/Z
        if ("V" in phasors) and ("Ohm" in phasors):  
            return phasors["V"] / phasors["Ohm"]
        # Z = U/I
        if ("V" in phasors) and ("A" in phasors):
            return phasors["V"] / phasors["A"]


    # This can be one function that returns a dict.
    def activePower(self):
        pass

    def reactivePower(self):
        pass

    def apparentPower(self):
        pass
    #---------------------------------------------

    def calculateImpedance(self, R: float = 0, L: float = 0, C: float = 0 , frequency: float = 0) -> Phasor:
        omega = math.pi * 2 * frequency
        x_l = omega * L
        x_c = 1/(omega*C)
        x_t = x_c - x_l
        return Phasor.fromComplex(R, x_t)


    # Series of voltage and current sources?
    def series(self, values: list[Phasor]) -> Phasor:
        return sum(values)

    # parallel of voltage and current sources?
    def parallel(self, values: list[Phasor]) -> Phasor:
        y = []
        for p in values:
            y.append(Phasor.getAdmitanceFromZ(p))

        return Phasor.getImpedanceFromY(sum(y))
    


