import matplotlib.pyplot as plt
import numpy as np


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
    

def calculate_tP(joint_efficiency, internal_pressure, radius, allowable_stress,type="cylinder",is_outer = False):
    E = joint_efficiency
    P = internal_pressure
    R = radius
    S = allowable_stress

    if type=="cylinder":

        tc = P*R/(S*E-0.6*P)
        Pc = S*E*tc/(R+0.6*tc)
        if tc > 0.5*R or Pc >0.385*S*E:
            print("WARNING: Thin shell criteria not met!")
        
        tl = P*R/(2*S*E+0.4*P)
        # STANDARD PLATE THICKNESS TO BE ADDED LATER
        Pl = 2*S*E*tl/(R-0.4*tl)

        t = (tc,tl)
        P = (Pc,Pl)

    elif type=="hemispherical":
        t = P*R/(2*S*E-0.2*P)
        if t < 0.356*R:
            print("WARNING: t < 0.356R")
        if t > 0.665*S*E:
            print("WARNING: t > 0.665SE")
        
        P = 2*S*E*t/(R+0.2*t)

    elif type=="elliptical21":
        t = P*R*2/(2*S*E-0.2*P)
        P = 2*S*E*t/(2*R+0.2*t)

    elif type=="torispherical":
        # NOT VERIFIED
        t = P*R/(2*S*E-0.2*P)
        if t < 0.356*R:
            print("WARNING: t < 0.356R")
        if t > 0.665*S*E:
            print("WARNING: t > 0.665SE")
        
        P = 2*S*E*t/(R+0.2*t)


    return t,P

def corrosion_allowance(stainless_steel=False):
    if stainless_steel:
        return 0.125
    else:
        return 0
        
def forming_allowance():
    return 0.0625

if __name__ == "__main__":
    # name = "SA-240g304plateNP"
    # standard = "ASME"
    # material = Material(name,standard)
    # material.product_form = "Plate"
    # temperature_yield = np.array([100, 200, 300, 400, 500, 600, 650, 700,
    #                                          750, 800, 850, 900, 950, 1000, 1050, 1100,
    #                                          1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500])

    # # print(temperature_yield.shape)
    # stress_yield = np.array([20.0, 16.7, 15.0, 13.8, 12.9, 12.3, 12.0, 11.7,
    #                                  11.5, 11.2, 11.0, 10.8, 10.6, 10.4, 10.1, 
    #                                  9.8, 7.7, 6.1, 4.7, 3.7, 2.9, 2.3, 1.8, 1.4])                                         
    # # print(stress_yield.shape)
    # material.setYieldStress(stress_yield, temperature_yield)

    # name2 = "SA-240g304plate800"
    # standard2 = "ASME"
    # material2 = Material(name2, standard2)
    # temperature_yield2 = temperature_yield
    # stress_yield2 = np.array([20.0, 20.0, 18.9, 18.3, 17.5, 16.6, 16.2, 15.8,
    #                                  15.5, 15.2, 14.9, 14.6, 14.3, 14.0, 12.4, 
    #                                  9.8, 7.7, 6.1, 4.7, 3.7, 2.9, 2.3, 1.8, 1.4])  

    
    # material2.setYieldStress(stress_yield2,temperature_yield2)
    # material.plotYieldStresses(material2)
    
    
    standard = "ASME"
    shell_material = Material("SA-516-70N",standard)

    join_efficiency = 0.85
    internal_pressure = 625 #psi
    internal_radius = (2*12+11)/2 #inch
    design_temp = 750 #F
    allowable_stress = 14800 #psi

    t, P = calculate_tP(join_efficiency,internal_pressure,internal_radius,allowable_stress)

    print(f"Thickness: {t}")
    print(f"Pressure: {P}")



