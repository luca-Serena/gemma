from abc import ABC, abstractmethod
from typing import Dict, List, TypeVar, Callable, Any

class GEMMA_Component (ABC):
    def __init__(self):
        self.parameters = {}

    @abstractmethod
    def retrieve_results(self, *args):
        #Retrieve the output from the GEMMA component. If it is the top-level component, then it provides the final results of the simulation. 
        pass

class GEMMA_Director (GEMMA_Component):

    def __init__(self):
        super().__init__()
        self.sub_models: Dict[GEMMA_Component] = {}

    @abstractmethod
    def call_sub_model (self, function: Callable[..., Any], *args):
        #Call an underlying sub-model. A function must be passed to identify the specific type of call.
        pass

    @abstractmethod
    def check_consistency(self, function: Callable[..., Any], *args):
        #Check the consistency of the the received data. A function must be passed to identify the specific type of call.
        pass

    @abstractmethod
    def check_call_conditions(self, function: Callable[..., Any] ,*args)-> bool:
        #Check the conditions for calling an underlying sub-model. A function must be passed to identify the specific type of call.
        pass

    @abstractmethod
    def instantiate_sub_models(self, *args):
        #Create an instance of the underlying sub-models
        pass