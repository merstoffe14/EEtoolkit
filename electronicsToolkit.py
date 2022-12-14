from ast import Str, arg
import math
import cmath
from math import radians
from mimetypes import init
from multiprocessing.sharedctypes import Value
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np

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
        if not z.unitCheck("Ohm"):
            raise ValueError("Z must be an impedance!")
        magnitude = 1/(z.getMagnitude())
        argument = -z.getArgument()
        return EEComplex.fromPolar(magnitude, argument, "S")

    def getImpedanceFromY(self, y: EEComplex) -> EEComplex:
        #check if y is an admitance
        if not y.unitCheck("S"):
            raise ValueError("Y must be an admitance!")
        magnitude = 1/(y.getMagnitude())
        argument = -y.getArgument()
        return EEComplex.fromPolar(magnitude, argument, "Ohm")

    def ohmsLaw(self, U: EEComplex= None, I: EEComplex = None, Z: EEComplex = None) -> EEComplex:
        # Check for unit errors maybe?
        if U and I:
            return U/I
        elif U and Z:
            return U/Z
        elif I and Z:
            return I*Z
        else:
            raise ValueError("You must provide 2 out of 3 variables")
        

    
    # # This can be one function that returns a dict.
    # I can make a class for this, but I don't know if it is worth it.
    # def activePower(self):
    #     pass

    # def reactivePower(self):
    #     pass

    # def apparentPower(self):
    #     pass
    # #---------------------------------------------

    def calculateImpedance(self, R: float = 0, L: float = 0, C: float = 0 , frequency: float = 0) -> EEComplex:
        omega = math.pi * 2 * frequency
        x_l = omega * L
        x_c = 1/(omega*C)
        x_t = x_c - x_l
        return EEComplex.fromComplex(R, x_t, "Ohm")


    # Series of voltage and current sources?
    def seriesImpedance(self, values: list[EEComplex]) -> EEComplex:
        return sum(values)

    # parallel of voltage and current sources?
    def parallelImpedance(self, values: list[EEComplex]) -> EEComplex:
        y = []
        for p in values:
            y.append(self.getAdmitanceFromZ(p))

        return self.getImpedanceFromY(sum(y))

    # Time in ms
    def drawScopeView(self, phasors: list[EEComplex], time: int = 100, sampleRate: int = 1000):
        x = np.linspace(0, time/1000, 1000)
        for p in phasors:
            #Check if phasor has a unit of V or A
            if not p.unitCheck("V") and not p.unitCheck("A"):
                raise ValueError("Phasor must be a voltage or current source!")
            else:
                # Multiplied by a factor of sqrt(2), to convert from RMS to peak, since phasors are always pure sinusoidal waves
                y = np.sqrt(2) * p.getMagnitude() * np.sin(2 * np.pi * p.frequency * x + radians(p.getArgument()))
                plt.plot(x,y)
      
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)/ Current (A)')
        plt.title('Scope View')
        # add function labels
        
        plt.show()