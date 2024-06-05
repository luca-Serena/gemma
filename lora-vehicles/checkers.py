class CallConditionsChecker():

	def checkCallConditionsMobility(self, submodel, *args):
		pass

	def checkCallConditionsODE (self, submodel, *args):   #the ODE model is called every update_frequency steps
		step, update_unit = args
		if step % self.parameters["update_frequency"] == update_unit and step > 0:
			return True
		else:
			return False

class ConsistencyChecker ():


	def checkConsistencyMobility (self,  submodel, *args):
		pass

	def checkConsistencyODE (self, submodel, *args):
		equipped_vehicles, normal_vehicles, service_cost = args
		c = self.parameters["initial_equipped_vehicles"] * self.parameters["initial_service_cost"]   #invariant of the program. It is allowed to vary under a defined margin of approximation
		loss = self.parameters["population"] - (equipped_vehicles + normal_vehicles)                 # ensure that the population remains stable over time
		if loss > 0:
			equipped_vehicles += loss
			#in case equipped vehicles * service cost exceed the margin of approximation re-establish the initial value of the product by changing service_cost
		if service_cost * equipped_vehicles >  c + self.parameters["margin_approximation"] or service_cost * equipped_vehicles < c - self.parameters["margin_approximation"]: 
			service_cost = c / equipped_vehicles
		return equipped_vehicles, normal_vehicles, service_cost
