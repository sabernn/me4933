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

class AssemblyBase(ABC):
    @abstractmethod
    def __init__(self,name) -> None:
        super().__init__()
        self.name = name
        self.ComponentList = None

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

class HeatExchanger(AssemblyBase):
    def __init__(self, name, material: Material, TEMAtype) -> None:
        super().__init__(name, material)
        self.TEMAtype = TEMAtype
        self.Datasheet = None

class Pipe(ComponentBase):
    def __init__(self, name, material: Material, nominal_diameter) -> None:
        super().__init__(name, material)
        self.nominal_diameter = nominal_diameter
        self.outside_diameter = None
        self.length = None
        self.alpha = None
        self.E = None
        self.W = None
        self.Y = None
        self.corrosion_allowance = None



    def calculate_thickness(self,design_pressure):
        P = design_pressure
        D = self.outside_diameter
        S = self.material.stress_yield[0]

        t = P * D / 2 / (S * self.E * self.W + P * self.Y)
        tm = t + self.corrosion_allowance + t*0.125
        return tm

    def thermal_expansion(self):
        return self.alpha * self.length
        

    def 

class Flange(ComponentBase):
    def __init__(self, name, material: Material, nominal_pipe_size, class_lb, type="RFWN") -> None:
        super().__init__(name, material)
        self.nominal_pipe_size = nominal_pipe_size
        self.class_lb = class_lb
        self.type = type
        self.is_dimension=False
        self.__flange_standard()
        

    def __flange_standard(self):
        if self.type=="RFWN":
            if self.nominal_pipe_size==8:
                self.outside_diameter = 13.5 #inch
                self.thickness_min = 1.125 #inch
                self.od_raised_face = 10.625 #inch
                self.d_hub_base = 9.6875 #inch
                self.bore = 7.98 #inch
                self.l_thru_hub = 4.0 #inch
                self.d_bevel_hub = 8.63 #inch
            else:
                print("Not implemented yet...")
                return None
        else:
            print("Not implemented yet...")
            return None

        self.is_dimension=True
        return self.outside_diameter,self.thickness_min,self.od_raised_face,self.d_hub_base,self.bore,self.l_thru_hub,self.d_bevel_hub

if __name__ == "__main__":
    material=Material("SA-516-70N","ASME")
    material.stress_yield = np.array([20000])
    material.temperature_yield = np.array([50])

    # vessel = PressureVessel("8PV-1752",material)

    flange = Flange("saber",material,8,150,"RFWN")

    O = flange.outside_diameter
    C = flange.thickness_min
    R = flange.od_raised_face



    # print(dir(flange))
    print(O)

    
    

    # print(dir(vessel))





