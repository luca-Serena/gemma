import os
import time
from GEMMA_Interfaces import GEMMA_Component, GEMMA_Director
from MobilityModel import MobilityModel
from ode_model import ODEModel


class Launcher (GEMMA_Director):

    def __init__ (self, params):#, sub_models):
        super().__init__()
        update_frequency, population, initial_equipped_vehicles, initial_service_cost, IoT_devices = params
        self.parameters["update_frequency"] = update_frequency
        self.parameters["population"] = population
        self.parameters["initial_equipped_vehicles"] = initial_equipped_vehicles
        self.parameters["initial_service_cost"] = initial_service_cost
        self.parameters["IoT_devices"] = IoT_devices


    def instantiate_sub_models (self, *args):
        modelPath, NetLogoPath, version = args
        mobilityModel = MobilityModel(modelPath, NetLogoPath, version)
        ode_model = ODEModel()
        self.sub_models ["mobility"] = mobilityModel
        self.sub_models ["ode"] = ode_model

    def check_consistency(self, function, *args):
        return function (*args)
    
    def check_consistency_ODE (self, *args): #todo
        equipped_vehicles, normal_vehicles, service_cost, margin_approximation = args
        c = self.parameters["initial_equipped_vehicles"] * self.parameters["initial_service_cost"]   #invariant of the program. It is allowed to vary under a defined margin of approximation
        loss = self.parameters["population"] - (equipped_vehicles + normal_vehicles)                 # ensure that the population remains stable over time
        if loss > 0:
            equipped_vehicles += loss
            #in case equipped vehicles * service cost exceed the margin of approximation re-establish the initial value of the product by changing service_cost
        if service_cost * equipped_vehicles >  c + margin_approximation or service_cost * equipped_vehicles < c - margin_approximation: 
            service_cost = c / equipped_vehicles
        return equipped_vehicles, normal_vehicles, service_cost


    def check_call_conditions (self, function, *args):
        return function(*args)

    def check_call_conditions_ODE (self, *args):
        step, update_unit= args
        if step % self.parameters["update_frequency"] == update_unit and step > 0:
            return True
        else:
            return False

    def call_sub_model (self, function, *args):
        return function(*args)

    def setup_netlogo (self):
        self.sub_models["mobility"].netlogo.command('setup ' + str(self.parameters["population"])  + " " + str(self.parameters["initial_equipped_vehicles"]) + " " + str(self.parameters["IoT_devices"]))

    def netlogo_advance (self):
        self.sub_models["mobility"].netlogo.command('go')

    def netlogo_update_vehicles (self, *args):
        current_equipped_vehicles = args[0]
        self.sub_models["mobility"].netlogo.command('update-vehicles ' + str(current_equipped_vehicles))  # update number of vehicles)

    def call_ODE_model (self, *args):
        current_equipped_vehicles, avgProfit = args
        return self.sub_models["ode"].run (current_equipped_vehicles, self.parameters["population"] - current_equipped_vehicles, avgProfit)


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
IoT_devices = 5

current_equipped_vehicles = initial_equipped_vehicles
service_cost = initial_service_cost
deliveries_over_time=[]
delay_over_time=[]
cost_over_time = []
equipped_vehicles_over_time = []
resultFile = "res.txt"


director = Launcher([update_frequency, population, initial_equipped_vehicles, initial_service_cost, IoT_devices])
director.instantiate_sub_models (modelPath, NetLogoPath, '6.0')

director.call_sub_model(director.setup_netlogo)     #intial setup of Netlogo (clear-all, reset-ticks)

for i in range (steps):
    if director.check_call_conditions (director.check_call_conditions_ODE, i, 0) == True:
        print ("current_equipped_vehicles: ", current_equipped_vehicles, " average profit", service_cost)
        current_equipped_vehicles, normal_vehicles, service_cost = director.call_sub_model (director.call_ODE_model, current_equipped_vehicles, service_cost)  # ODE model launched     
        current_equipped_vehicles, normal_vehicles, service_cost = director.check_consistency (director.check_consistency_ODE, current_equipped_vehicles, normal_vehicles, service_cost, 1)       
        print (" product: ", current_equipped_vehicles * service_cost)  

        delay =  int(director.sub_models["mobility"].getDelay())
        deliveries = int(director.sub_models["mobility"].getDeliveries())
        cost_over_time.append(service_cost)
        deliveries_over_time.append (deliveries)
        delay_over_time.append (0 if deliveries == 0 else delay/deliveries)
        equipped_vehicles_over_time.append (current_equipped_vehicles)
        director.call_sub_model(director.netlogo_update_vehicles, current_equipped_vehicles)


    director.call_sub_model(director.netlogo_advance)          
    time.sleep(0.005)     # in order to allow the user to visualize changes through time, otherwise it runs at maximum speed


director.retrieve_results(resultFile, cost_over_time, deliveries_over_time, delay_over_time, equipped_vehicles_over_time)
print ("Simulation Ended")