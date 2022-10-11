from ast import Str, arg
import math
import cmath
from math import radians
from mimetypes import init
from multiprocessing.sharedctypes import Value
from queue import Empty
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
import pint
from enum import Enum

from eecomplex import EEComplex


class EEToolkit:

   
    # I am not sure if you would use RMS or PEAK value for phasors, I need to check my handbook
    # In my head it would be PEAK value because then the phasor will draw the correct sinusoidal wave
    # But if I remember correctly we always use RMS
    # If we calculate a power, we use phasors using RMS (logical because for ac power calculations you need to use RMS)

  

    def __init__(self) -> None:

        self.standardValues = {
            "mains_us": EEComplex.fromComplex(120, 0, "V", 60),
            "mains": EEComplex.fromComplex(230, 0, "V", 50),
        } 
        

    def getAdmitanceFromZ(self, z: EEComplex) -> EEComplex: 
        #check if z is an impedance 
        if not (z.units[0].count("Ohm") and len(z.units[0]) == 1) and not z.units[1]:
            raise ValueError("Z must be an impedance!")
        magnitude = 1/(z.getMagnitude())
        argument = -z.getArgument()
        return EEComplex.fromPolar(magnitude, argument, "S")

    def getImpedanceFromY(self, y: EEComplex) -> EEComplex:
        #check if y is an admitance
        if not (y.units[0].count("S") and len(y.units[0]) == 1) and not y.units[1]:
            raise ValueError("Y must be an admitance!")
        magnitude = 1/(y.getMagnitude())
        argument = -y.getArgument()
        return EEComplex.fromPolar(magnitude, argument, "ohm")

    # def ohmsLaw(self, p1, p2) -> Phasor:

    #     # I can avoid using this dict by calling the function with ohmsLaw(x = .., y = ..) and  then working with default values.
    #     phasors = {
    #         p1.unit: p1,
    #         p2.unit: p2,
    #     }

    #     # U = ZI
    #     if ("Ohm" in phasors) and ("A" in phasors):
    #         return p1 * p2
    #     # I = U/Z
    #     if ("V" in phasors) and ("Ohm" in phasors):  
    #         return phasors["V"] / phasors["Ohm"]
    #     # Z = U/I
    #     if ("V" in phasors) and ("A" in phasors):
    #         return phasors["V"] / phasors["A"]


    # # This can be one function that returns a dict.
    # def activePower(self):
    #     pass

    # def reactivePower(self):
    #     pass

    # def apparentPower(self):
    #     pass
    # #---------------------------------------------

    # def calculateImpedance(self, R: float = 0, L: float = 0, C: float = 0 , frequency: float = 0) -> Phasor:
    #     omega = math.pi * 2 * frequency
    #     x_l = omega * L
    #     x_c = 1/(omega*C)
    #     x_t = x_c - x_l
    #     return Phasor.fromComplex(R, x_t)


    # # Series of voltage and current sources?
    # def series(self, values: list[Phasor]) -> Phasor:
    #     return sum(values)

    # # parallel of voltage and current sources?
    # def parallel(self, values: list[Phasor]) -> Phasor:
    #     y = []
    #     for p in values:
    #         y.append(Phasor.getAdmitanceFromZ(p))

    #     return Phasor.getImpedanceFromY(sum(y))

