import numpy as np
from scipy.integrate import odeint
from GEMMA_Interfaces import GEMMA_Component, GEMMA_Director
from MobilityModel import MobilityModel
from ode_model import ODEModel
from checkers import ConsistencyChecker, CallConditionsChecker


class ODEModel(GEMMA_Component):

    # Definition of differential equations
    def model(self, y, t, k, c):
        P, G = y
        # P represents the percentage of vehicles equipped for the reception of sensor data
        # G represents the average gain
        dPdt = k * G * (1 - P) 
        newP = P + k * G * (1 - P) 
        dGdt = - (G - c / newP )
        return [dPdt, dGdt]

    def setup():
        pass

    def advance (self, equipped, notEquipped, avgProfit):
        population = equipped + notEquipped
        P0 = equipped / (population)
        G0 = avgProfit
        y0 = [P0, avgProfit]        # Percentage of equipped vehicles and average profit per equipped vehicle
        
        # Internal parameters of the model
        k = 0.1  # stimulus for adopting sensor data reception equipment
        c = P0 * G0 #total amount of issued money

        # Time interval
        t = np.linspace(0, 0.5, 100)

        # Numerical solving of differential equations 
        y = odeint(self.model, y0, t, args=(k,c))

        return self.retrieve_results(y, population) 
        #return int(y[-1:, 0] * population), int((1 - y[-1:, 0]) * population), float (y[-1:, 1])


    def retrieve_results (self, y, population):
        equipped = int(y[-1:, 0] * population)
        notEquipped = int((1 - y[-1:, 0]) * population)
        avgProfit = float (y[-1:, 1])
        return [equipped, notEquipped, avgProfit]

    def check_call_conditions(self, checker, *args):
        return checker.checkCallConditionsODE(self,*args)

    def check_consistency (self, checker, *args):
        return checker.checkConsistencyODE(self, *args)

