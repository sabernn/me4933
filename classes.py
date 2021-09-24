from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
import Standards.ASME as ASME

class DimensionBase(ABC):
    @abstractmethod
    def __init__(self, value, tol_l, tol_u):
        super().__init__()
        self.value = value
        self.tol_l = tol_l
        self.tol_u = tol_u
        self.min = self.value + self.tol_l
        self.max = self.value + self.tol_u

class Material:
    def __init__(self, name, standard):
        self.name = name
        self.standard = standard
        self.pp = None
        self.product_form = None
        self.stress_yield = None
        self.temperature_yield = None
        

    def setYieldStress(self,stress_yield,temperature_yield, plot=True):
        if stress_yield.shape != temperature_yield.shape:
            raise ValueError("Yield and temperature vectors not in the same size!")
            return None
        self.stress_yield = stress_yield
        self.temperature_yield = temperature_yield
        if plot:
            if self.stress_yield == "":
                raise ValueError("Noting to plot!")
            plt.plot(self.temperature_yield, self.stress_yield)
            plt.plot(self.temperature_yield, self.stress_yield, 'o')
            plt.xlabel("Temperature (F)")
            plt.ylabel("Yield stress (ksi)")
            plt.title(f"Yield stress versus Temperature for Material {self.name}")
            plt.show()
        return stress_yield, temperature_yield


    def plotYieldStresses(self, material2= None):
        if self.stress_yield.shape[0] == 0 or material2.stress_yield.shape[0] == 0:
            raise ValueError("At least one material does not have enough data.")
        plt.plot(self.temperature_yield, self.stress_yield)
        plt.plot(material2.temperature_yield, material2.stress_yield)
        plt.plot(self.temperature_yield, self.stress_yield, 'o')
        plt.plot(material2.temperature_yield, material2.stress_yield, 'd')
        plt.legend([self.name, material2.name])
        plt.xlabel("Temperature (F)")
        plt.ylabel("Yield stress (psi)")
        plt.title(f"Yield stress versus Temperature for Materials {self.name} and {material2.name}")
        plt.show()


class ComponentBase(ABC):
    @abstractmethod
    def __init__(self,name,material: Material) -> None:
        super().__init__()
        self.name = name
        self.material = material

    def design(self):
        pass

    def exportCAD(self):
        pass



class PressureVessel(ComponentBase):
    def __init__(self, name, material: Material) -> None:
        super().__init__(name, material)
        self.inner_radius = None
        self.design_pressure = None
        self.design_temperature = None
        self.headtype = None
        self.shell_joint_efficiency = None
        self.head_joint_efficiency = None
        self.shell_thickness = None
        self.head_thickness = None
        self.designed = False

    def CalculateThickness(self):
        E = self.shell_joint_efficiency
        P = self.design_pressure
        R = self.inner_radius
        S = self.material.stress_yield[0]

        return ASME.calculate_tP(E,P,R,S)


if __name__ == "__main__":
    material=Material("SA-516-70N","ASME")
    material.stress_yield = np.array([20000])
    material.temperature_yield = np.array([50])

    vessel = PressureVessel("8PV-1752",material)

    print(dir(vessel))





