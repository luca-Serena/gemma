import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definizione delle equazioni differenziali
def model(y, t, k, c):
    P, G = y
    # P represents the percentage of lora-equipped vehicles
    # G represents the average gain
    dPdt = k * G * (1 - P) 
    newP = P + k * G * (1 - P) 
    dGdt = - (G - c / newP )
    return [dPdt, dGdt]


def run (equipped, notEquipped, avgProfit):
    population = equipped + notEquipped
    P0 = equipped / (population)
    G0 = avgProfit
    y0 = [P0, avgProfit]        # Percentage of lora-equipped vehicles and average profit per LoRa-equipped vehicle
    
    # Internal parameters of the model
    k = 0.1  # stimulus for adopting LoRa equipment
    c = P0 * G0 #total amount of issued money

    # Time interval
    t = np.linspace(0, 1, 100)

    # Numerical solving of differential equations 
    y = odeint(model, y0, t, args=(k,c))

    return int(y[-1:, 0] * population), int((1 - y[-1:, 0]) * population), float (y[-1:, 1])