# Multilevel Modeling and Simulation. Smart City Use Case

## Models employed
- an ODE model that describes variation of vehicles equipped to receive sensor data and the cost of the service
- cellular automaton mobility model, developed with NetLogo

## Important Parameters

- steps = number of netLogo steps
- update-frequency = frequency for the call of ODE modell. Also, we assume that new data are sent every update-frequency Netlogo steps
- population = number of vehicles agents in the model
- initial-equipped-vehicles = number of vehicles equipped for receiving sensor data from the beginning
- initial-service-cost = amount of money/tokens that acts as a reward for the service of the vehicles
- Iot-Devices = number of IoT sensors in the simulated environment

## Requirements
The following Python packages are required:
- numpy
- scipy
- pyNetLogo

Furthermore, NetLogo software must be installed


## Usage
The user has to open `launcher.py` file and then set the path of NetLogo executable and the path of .nlogo model
Then, to run just execute `python3 launcher.py`


### Outputs

In res.txt


## Contacts

Luca Serena <luca.serena2@unibo.it>


