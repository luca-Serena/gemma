class CallConditionsChecker():

	def checkCallConditionsMobility(self, submodel, *args):
		pass


	def checkCallConditionsODE (self, submodel, *args):

		step, update_step = args
		if step % self.parameters["update_frequency"] == update_step:
			return True
		else:
			return False		



class ConsistencyChecker ():

	def checkConsistencyMobility (self,  submodel, *args):
		pass

	def checkConsistencyODE (self, submodel, *args):
		petroil, GPL, electric = args
		loss = self.parameters["population"] - (petroil + GPL + electric)
		if loss == 0:
			return petroil, GPL, electric
		else:
			return self.valuesRounding (loss, [petroil, GPL, electric])
		
		'''
		equipped_vehicles, normal_vehicles, service_cost = args
		c = self.parameters["initial_equipped_vehicles"] * self.parameters["initial_service_cost"]   #invariant of the program. It is allowed to vary under a defined margin of approximation
		loss = self.parameters["population"] - (equipped_vehicles + normal_vehicles)                 # ensure that the population remains stable over time
		if loss > 0:
			equipped_vehicles += loss
			#in case equipped vehicles * service cost exceed the margin of approximation re-establish the initial value of the product by changing service_cost
		if service_cost * equipped_vehicles >  c + self.parameters["margin_approximation"] or service_cost * equipped_vehicles < c - self.parameters["margin_approximation"]: 
			service_cost = c / equipped_vehicles
		return equipped_vehicles, normal_vehicles, service_cost
		'''

	def valuesRounding (self, howMany, valueList):
		returnList = [int(elem) for elem in valueList]          # list of values to return. Continuous values are discretized
		tempList = [elem - int(elem) for elem in valueList]     # temporary list with only the fractional part of the considered values
		for i in range (howMany):                               # howMany depends on the total loss
			max_value = max(tempList)                           # number with the highest fractional part
			max_index = tempList.index(max_value)               # index with of the number with the highest fractional part
			tempList[max_index] = -1                            # to ignore in the future
			returnList [max_index] += 1                         # element of the list rounded up 
		return returnList
	