from abc import ABC, abstractmethod

class Director_Interface(ABC):

    parameters = None
    sub_models = None

    @abstractmethod
    def check_consistency(self, function, *args):
        pass

    @abstractmethod
    def check_call_conditions(self, function ,*args):
        pass

    @abstractmethod
    def call_sub_model (self, function, *args):
        pass

    @abstractmethod
    def print_results(self, *args):
        pass


