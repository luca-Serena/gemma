import os
import time
from GEMMA_Interfaces import GEMMA_Component, GEMMA_Director
from MobilityModel import MobilityModel
from ode_model import ODEModel
from checkers import ConsistencyChecker, CallConditionsChecker


class Launcher (GEMMA_Director):

    def __init__ (self, params):#, sub_models):
        super().__init__()
        update_frequency, population, initial_equipped_vehicles, initial_service_cost, IoT_devices, margin_approximation = params
        self.parameters["update_frequency"] = update_frequency
        self.parameters["population"] = population
        self.parameters["initial_equipped_vehicles"] = initial_equipped_vehicles
        self.parameters["initial_service_cost"] = initial_service_cost
        self.parameters["IoT_devices"] = IoT_devices
        self.parameters["margin_approximation"] = margin_approximation


    def instantiate_sub_models (self, *args):
        modelPath, NetLogoPath, version = args
        mobilityModel = MobilityModel(modelPath, NetLogoPath, version)
        ode_model = ODEModel()
        self.sub_models ["mobility"] = mobilityModel
        self.sub_models ["ode"] = ode_model


    def setup():
        pass

    def advance():
        pass

    def check_consistency(self, *args):
        pass 

    def check_call_conditions (self, *args):
        pass        

    def retrieve_results (self, *args):
        resFile, cost_list, deliveries_list, delay_list, vehicle_list = args 
        with open (resFile, "w") as file:
            for index, elem in enumerate (cost_list):
                file.write ("At timestep " + str((index + 1) * self.parameters["update_frequency"]) + " cost for service: " +
                 str(round(elem, 2)) + " with " + str(vehicle_list[index]) + " equipped vehicles. Deliveries: " + 
                 str(deliveries_list[index]) + " with average delay: " + str(round(delay_list[index], 2)) + "\n")


############################################################################################################################################################




NetLogoPath = '/home/senecaurla/Downloads/NetLogo'
modelPath = '/home/senecaurla/Documents/phd/gemma/lora-vehicles/mobility.nlogo'
steps = 1001
update_frequency=50
population = 100
initial_equipped_vehicles = 10
initial_service_cost = 1
#the product between the service cost and the number of equipped vehicles should be costant (allowing a certain margin of approximation)
margin_approximation = 1
IoT_devices = 5

current_equipped_vehicles = initial_equipped_vehicles
service_cost = initial_service_cost
deliveries_over_time=[]
delay_over_time=[]
cost_over_time = []
equipped_vehicles_over_time = []
resultFile = "res.txt"


director = Launcher([update_frequency, population, initial_equipped_vehicles, initial_service_cost, IoT_devices, margin_approximation])
director.instantiate_sub_models (modelPath, NetLogoPath, '6.0')
consistency_checker = ConsistencyChecker (director)
conds_checker = CallConditionsChecker(director)

director.sub_models["mobility"].setup(population, initial_equipped_vehicles, IoT_devices)    #intial setup of Netlogo (clear-all, reset-ticks)

for i in range (steps):
    if director.sub_models["ode"].check_call_conditions (conds_checker, i, 0) == True:
        print ("current_equipped_vehicles: ", current_equipped_vehicles, " average profit", service_cost)
        current_equipped_vehicles, normal_vehicles, service_cost = director.sub_models["ode"].advance(current_equipped_vehicles, population - current_equipped_vehicles, service_cost)  # ODE model launched     
        current_equipped_vehicles, normal_vehicles, service_cost = director.sub_models["ode"].check_consistency(consistency_checker, current_equipped_vehicles, normal_vehicles, service_cost)
        print (" product: ", current_equipped_vehicles * service_cost)  

        delay =  director.sub_models["mobility"].getDelay()
        deliveries = director.sub_models["mobility"].getDeliveries()
        cost_over_time.append(service_cost)
        deliveries_over_time.append (deliveries)
        delay_over_time.append (0 if deliveries == 0 else delay/deliveries)
        equipped_vehicles_over_time.append (current_equipped_vehicles)
        director.sub_models["mobility"].update_vehicles(current_equipped_vehicles)

    director.sub_models["mobility"].advance()         
    time.sleep(0.005)     # in order to allow the user to visualize changes through time, otherwise it runs at maximum speed


director.retrieve_results(resultFile, cost_over_time, deliveries_over_time, delay_over_time, equipped_vehicles_over_time)
print ("Simulation Ended")