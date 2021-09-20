



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