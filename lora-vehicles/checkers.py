class CallConditionsChecker():

	def __init__ (self, director):
		self.director = director

	def checkCallConditionsMobility(self):
		pass

	def checkCallConditionsODE (self, *args):
		step, update_unit= args
		if step % self.director.parameters["update_frequency"] == update_unit and step > 0:
			return True
		else:
			return False

class ConsistencyChecker ():

	def __init__ (self, director):
		self.director = director

	def checkConsistencyMobility (self, *args):
		pass

	def checkConsistencyODE (self, *args):
		equipped_vehicles, normal_vehicles, service_cost = args
		c = self.director.parameters["initial_equipped_vehicles"] * self.director.parameters["initial_service_cost"]   #invariant of the program. It is allowed to vary under a defined margin of approximation
		loss = self.director.parameters["population"] - (equipped_vehicles + normal_vehicles)                 # ensure that the population remains stable over time
		if loss > 0:
			equipped_vehicles += loss
			#in case equipped vehicles * service cost exceed the margin of approximation re-establish the initial value of the product by changing service_cost
		if service_cost * equipped_vehicles >  c + self.director.parameters["margin_approximation"] or service_cost * equipped_vehicles < c - self.director.parameters["margin_approximation"]: 
			service_cost = c / equipped_vehicles
		return equipped_vehicles, normal_vehicles, service_cost
