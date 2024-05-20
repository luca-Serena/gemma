from GEMMA_Interfaces import GEMMA_Component
from checkers import CallConditionsChecker, ConsistencyChecker
import pyNetLogo

class MobilityModel(GEMMA_Component):

	def __init__(self, modelPath, NetLogoPath, version):
		self.netlogo = pyNetLogo.NetLogoLink(gui=True, netlogo_home=NetLogoPath, netlogo_version=version)  # Linking with NetLogo
		self.netlogo.load_model(modelPath)  

	def setup (self, *args):
		population, initial_equipped_vehicles, IoT_devices = args
		self.netlogo.command('setup ' + str(population)  + " " + str(initial_equipped_vehicles) + " " + str(IoT_devices))

	def advance(self):
		self.netlogo.command('go')

	def retrieve_results (self, *args):
		 pass

	def check_call_conditions (self, checker):
		pass

	def check_consistency(self, checker):
		pass

	def getDelay (self):
		return int(self.netlogo.report ("delay"))

	def getDeliveries(self):
		return int(self.netlogo.report ("deliveries"))

	def update_vehicles (self, new_vehicles):
		self.netlogo.command('update-vehicles ' + str(new_vehicles))  # update number of vehicles)
