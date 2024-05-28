from GEMMA_Interfaces import GEMMA_Component
from checkers import CallConditionsChecker, ConsistencyChecker
import pyNetLogo

class MobilityModel(GEMMA_Component):

	def __init__(self, modelPath, NetLogoPath, version):
		self.netlogo = pyNetLogo.NetLogoLink(gui=True, netlogo_home=NetLogoPath, netlogo_version=version)  # Linking with NetLogo
		self.netlogo.load_model(modelPath)  

	def setup (self, population):
		self.netlogo.command('setup ' + str(population)) 

	def advance(self):
		self.netlogo.command('go')

	def retrieve_results (self, *args):
		 pass

	def check_call_conditions (self, checker):
		pass

	def check_consistency(self, checker):
		pass

	def getPollution (self):
		return int (self.netlogo.report ("sum [ pollution ] of patches"))

	def update_vehicles (self, petroil, GPL, electric ):
		self.netlogo.command('update-vehicles ' + str(int(petroil)) + ' ' + str(int(GPL)) + ' ' + str(int(electric)) )	# update number of vehicles
