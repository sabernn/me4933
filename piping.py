



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
    





