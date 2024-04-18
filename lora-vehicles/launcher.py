import pandas as pd
import numpy as np
from scipy import stats
import os
import pyNetLogo
import ode_lora
import json
import time
from Director_Interface import Director_Interface


class Launcher (Director_Interface):

    def __init__ (self, parameters, sub_models):
        self.update_frequency, self.population, self.initial_lora_vehicles, self.IoT_devices = parameters
        self.netlogo, self.ode_lora = sub_models

    def check_consistency(self, function, *args):
        return function (*args)
    
    def check_consistency_ODE (self, *args): #todo
        lora_vehicles, normal_vehicles = args
        loss = self.population - (lora_vehicles + normal_vehicles)
        if loss == 0:
            return lora_vehicles
        else:
            return lora_vehicles + loss

    def check_call_conditions (self, function, *args):
        return function(*args)

    def check_call_conditions_ODE (self, *args):
        step, update_unit= args
        if step % self.update_frequency == update_unit and step > 0:
            return True
        else:
            return False


    def call_sub_model (self, function, *args):
        return function(*args)

    def setup_netlogo (self):
        self.netlogo.command('setup ' + str(self.population)  + " " + str(self.initial_lora_vehicles) + " " + str(self.IoT_devices))

    def netlogo_advance (self):
        self.netlogo.command('go')

    def netlogo_update_vehicles (self, *args):
        current_lora_vehicles = args[0]
        self.netlogo.command('update-vehicles ' + str(current_lora_vehicles))  # update number of vehicles)

    def call_ODE_model (self, *args):
        current_lora_vehicles, avgProfit = args
        return self.ode_lora.run (current_lora_vehicles, self.population - current_lora_vehicles, avgProfit)


    def print_results (self, *args):
        resFile, cost_list, deliveries_list, delay_list = args 
        with open (resFile, "w") as file:
            for index, elem in enumerate (cost_list):
                file.write ("At timestep " + str((index + 1) * self.update_frequency) + " cost: " + str(elem) + " deliveries " + str(deliveries_list[index]) + " delay " + str(delay_list[index]) + "\n")


############################################################################################################################################################




NetLogoPath = '/home/senecaurla/Downloads/NetLogo'
modelPath = '/home/senecaurla/Documents/phd/gemma/lora-vehicles/mobility.nlogo'
steps = 501
update_frequency=50
population = 100
initial_lora_vehicles = 10
IoT_devices = 5

current_lora_vehicles = initial_lora_vehicles
service_cost = 1
deliveries_over_time=[]
delay_over_time=[]
cost_over_time = []
resultFile = "res.txt"

netlogo = pyNetLogo.NetLogoLink(gui=True, netlogo_home=NetLogoPath, netlogo_version='6.0')  # Linking with NetLogo
netlogo.load_model(modelPath)                                                               # Load the Model


director = Launcher([update_frequency, population, initial_lora_vehicles, IoT_devices], [netlogo, ode_lora])


director.call_sub_model(director.setup_netlogo)     #intial setup of Netlogo (clear-all, reset-ticks)

for i in range (steps):
    if director.check_call_conditions (director.check_call_conditions_ODE, i, 0) == True:
        print ("params: ", current_lora_vehicles, " ", service_cost)
        current_lora_vehicles, normal_vehicles, service_cost = director.call_sub_model (director.call_ODE_model, current_lora_vehicles, service_cost)  # ODE model launched     
        #print ("at ", i, " petroil: ", petroil, " GPL: ", GPL, " electric: ", electric)
        current_lora_vehicles = director.check_consistency (director.check_consistency_ODE, current_lora_vehicles, normal_vehicles)       
        print (current_lora_vehicles, "  ", service_cost, " product: " , current_lora_vehicles * service_cost)  

        delay =  int(netlogo.report ("delay"))
        deliveries = int(netlogo.report ("deliveries"))
        delay_over_time.append(delay)
        cost_over_time.append(service_cost)
        deliveries_over_time.append (deliveries)
        delay_over_time.append (0 if deliveries == 0 else delay/deliveries)

        director.call_sub_model(director.netlogo_update_vehicles, current_lora_vehicles)


    director.call_sub_model(director.netlogo_advance)           
     
    time.sleep(0.005)                                # in order to allow the user to visualize changes through time, otherwise it runs at maximum speed


director.print_results(resultFile, cost_over_time, deliveries_over_time, delay_over_time)