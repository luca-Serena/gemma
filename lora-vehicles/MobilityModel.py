from GEMMA_Interfaces import GEMMA_Component
import pyNetLogo

class MobilityModel(GEMMA_Component):

	def __init__(self, modelPath, NetLogoPath, version):
		self.netlogo = pyNetLogo.NetLogoLink(gui=True, netlogo_home=NetLogoPath, netlogo_version='6.0')  # Linking with NetLogo
		self.netlogo.load_model(modelPath)  

	def retrieve_results (self, *args):
		 pass





