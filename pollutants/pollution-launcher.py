import pandas as pd
import numpy as np
from scipy import stats
import os
import pyNetLogo
import odepollution
import json
import time
from Director_Interface import Director_Interface


class Pollution_Launcher (Director_Interface):

    def __init__ (self, parameters, sub_models):
        self.update_frequency, self.population = parameters
        self.netlogo, self.odepollution = sub_models

    def check_consistency(self, function, *args):
        return function (*args)
    
    def check_consistency_ODE (self, *args):
        petroil, GPL, electric = args
        loss = self.population - (petroil + GPL + electric)
        if loss == 0:
            return petroil, GPL, electric
        else:
            return self.valuesRounding (loss, [petroil, GPL, electric])

    def check_call_conditions (self, function, *args):
        return function(*args)

    def check_call_conditions_ODE (self, *args):
        step, update_step = args
        if step % self.update_frequency == update_step:
            print (step, " ", update_frequency)
            return True
        else:
            return False


    def call_sub_model (self, function, *args):
        return function(*args)

    def setup_netlogo (self):
        self.netlogo.command('setup ' + str(self.population))

    def netlogo_advance (self):
        self.netlogo.command('go')

    def netlogo_update_vehicles (self, *args):
        petroil, GPL, electric = args
        self.netlogo.command('update-vehicles ' + str(int(petroil)) + ' ' + str(int(GPL)) + ' ' + str(int(electric)) )  # update number of vehicles)

    def call_ODE_model (self, *args):
        petroil, GPL, electric, pollution = args
        return self.odepollution.run (petroil, GPL, electric, pollution/10000)


    def print_results (self, *args):
        resFile, resList = args 
        with open (resFile, "w") as file:
            for index, elem in enumerate (resList):
                file.write ("At timestep " + str(index * self.update_frequency) + " pollution: " + str(elem) + "\n")

    def valuesRounding (self, howMany, valueList):
        returnList = [int(elem) for elem in valueList]          # list of values to return. Continuous values are discretized
        tempList = [elem - int(elem) for elem in valueList]     # temporary list with only the fractional part of the considered values
        for i in range (howMany):                               # howMany depends on the total loss
            max_value = max(tempList)                           # number with the highest fractional part
            max_index = tempList.index(max_value)               # index with of the number with the highest fractional part
            tempList[max_index] = -1                            # to ignore in the future
            returnList [max_index] += 1                         # element of the list rounded up 

        return returnList



############################################################################################################################################################




NetLogoPath = '/home/senecaurla/Downloads/NetLogo'
modelPath = '/home/senecaurla/Documents/phd/gemma/pollutants/pollution.nlogo'
steps = 3000
update_frequency=30
population = 200
pollution_over_time=[]
resultFile = "res.txt"

netlogo = pyNetLogo.NetLogoLink(gui=True, netlogo_home=NetLogoPath, netlogo_version='6.0')  # Linking with NetLogo
netlogo.load_model(modelPath)                                                               # Load the Model


director = Pollution_Launcher([update_frequency, population], [netlogo, odepollution])


director.call_sub_model(director.setup_netlogo)
#netlogo.command('setup ' + str(population) )       #intial setup of Netlogo (clear-all, reset-ticks)

petroil = population
electric = 0
GPL = 0

for i in range (steps):
    director.call_sub_model(director.netlogo_advance)   
    check_call_args = [i, update_frequency, 10]
    if director.check_call_conditions (director.check_call_conditions_ODE, i, 10) == True:
        pollution =  netlogo.report ("sum [ pollution ] of patches")
        #print ("pollution: " + str(pollution))
        pollution_over_time.append(pollution)
        petroil, GPL, electric = director.call_sub_model (director.call_ODE_model, petroil, GPL, electric, pollution)    # compartmental model launched     
        #print ("at ", i, " petroil: ", petroil, " GPL: ", GPL, " electric: ", electric)
        petroil, GPL, electric = director.check_consistency (director.check_consistency_ODE, petroil, GPL, electric)         
        #print ("after--> petroil: ", petroil, " GPL: ", GPL, " electric: ", electric)                        
        director.call_sub_model(director.netlogo_update_vehicles, petroil, GPL, electric)
        print (str(int(petroil)) + ' ' + str(int(GPL)) + ' ' + str(int(electric)))
        
     
    time.sleep(0.001)                                # in order to allow the user to visualize changes through time, otherwise it runs at maximum speed


director.print_results(resultFile, pollution_over_time)