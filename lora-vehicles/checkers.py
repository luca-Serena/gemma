class CallConditionsChecker():

	def checkCallConditionsMobility(self, director, *args):
		pass

	def checkCallConditionsODE (self, director, *args):
		step, update_unit = args
		if step % director.parameters["update_frequency"] == update_unit and step > 0:
			return True
		else:
			return False

class ConsistencyChecker ():


	def checkConsistencyMobility (self,  director, *args):
		pass

	def checkConsistencyODE (self, director, *args):
		equipped_vehicles, normal_vehicles, service_cost = args
		c = director.parameters["initial_equipped_vehicles"] * director.parameters["initial_service_cost"]   #invariant of the program. It is allowed to vary under a defined margin of approximation
		loss = director.parameters["population"] - (equipped_vehicles + normal_vehicles)                 # ensure that the population remains stable over time
		if loss > 0:
			equipped_vehicles += loss
			#in case equipped vehicles * service cost exceed the margin of approximation re-establish the initial value of the product by changing service_cost
		if service_cost * equipped_vehicles >  c + director.parameters["margin_approximation"] or service_cost * equipped_vehicles < c - director.parameters["margin_approximation"]: 
			service_cost = c / equipped_vehicles
		return equipped_vehicles, normal_vehicles, service_cost
