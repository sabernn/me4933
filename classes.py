from abc import ABC, abstractmethod

class DimensionBase(ABC):
    @abstractmethod
    def __init__(self, value, tol_l, tol_u):
        self.value = value
        self.tol_l = tol_l
        self.tol_u = tol_u
        self.min = self.value + self.tol_l
        self.max = self.value + self.tol_u

    

