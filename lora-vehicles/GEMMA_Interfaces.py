from abc import ABC, abstractmethod
from typing import List

class GEMMA_Component (ABC):
    parameters = None

    @abstractmethod
    def retrieve_results(self, *args):
        pass

class GEMMA_Director (GEMMA_Component):

    sub_models: List[GEMMA_Component] = []

    @abstractmethod
    def check_consistency(self, function, *args):
        pass

    @abstractmethod
    def check_call_conditions(self, function ,*args)-> bool:
        pass

    @abstractmethod
    def call_sub_model (self, function, *args):
        pass

    @abstractmethod
    def instantiate_sub_models(self, sub_models)-> List[GEMMA_Component]:
        pass


