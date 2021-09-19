
from math import *



def calc_thickness(design_pressure, outer_diameter, allowable_stress, E, W, Y, corrosion_allowance):
    P = design_pressure
    D = outer_diameter
    S = allowable_stress

    t = P*D/2/(S*E*W+P*Y)
    tm = t + corrosion_allowance + t*0.125
    return tm

def thermal_expansion(alpha,length):
    delta = alpha*length
    return delta

def wave_velocity_steel(inside_diameter,min_thickness):
    d = inside_diameter #inch
    t = min_thickness #inch
    a = 4660/(1+(d/100/t))**0.5 #ft/s
    return a

def water_hammer_pressure(wave_speed,fluid_density,fluid_velocity):
    g = 32.17405 #ft/s2
    a = wave_speed #ft/s
    W = fluid_density #lbs/ft3
    V = fluid_velocity #ft/s
    P = a*W*V/(144*g) #psi
    return P

def water_hammer_force(pressure_spike, inside_diameter):
    area = pi/4*inside_diameter**2
    F = pressure_spike*area
    return F

if __name__ == "__main__":
    design_pressure = 300 #psig
    outer_diameter = 6.625 #inch
    allowable_stress = 14800 #psi
    E = 0.85
    W = 1.0
    Y = 0.4
    corrosion_allowance = 0.0 #inch
    tm = calc_thickness(design_pressure,outer_diameter,allowable_stress,E,W,Y,corrosion_allowance)
    print(f"Minimum thickness of pipe: tm = {tm}")

    alpha = 0.0316 #inch/ft
    L = 300 #ft
    delta = thermal_expansion(alpha,L)
    print(f"Thermal expansion of pipe: d = {delta}")

    # HW3 P3
    fluid_velocity = 10 #ft/sec
    fluid_density = 62.4 #lbs/ft3
    diameter_nominal = 24 #inch
    diameter_outer = 24.0 #from table
    pressure = 100 #psig
    allowable_stress = 20000 #psi
    E = 0.85
    W = 1.0
    Y = 0.4
    corrosion_allowance = 0.125 #inch (for carbon steel)
    thickness = calc_thickness(design_pressure=pressure,
                        outer_diameter=diameter_outer,
                        allowable_stress=allowable_stress,
                        E=E, W=W, Y=Y, 
                        corrosion_allowance=corrosion_allowance)
    
    diameter_inner = diameter_outer-thickness
    wave_speed = wave_velocity_steel(diameter_inner,thickness)
    P = water_hammer_pressure(wave_speed,fluid_density,fluid_velocity)
    F = water_hammer_force(P,diameter_inner)
    print("\n\nHW3 P3")
    print(f"tm {thickness}")
    print(f"a {wave_speed}")
    print(f"P_wh {P}")
    print(f"F_wh {F}")




    





