import matplotlib.pyplot as plt
import numpy as np
from classes import Material, Flange


    

def flange_standard(nominal_pipe_size,flange_type):
    if flange_type=="RFWN":
        if nominal_pipe_size==8:
            outside_diameter = 13.5 #inch
            thickness_min = 1.125 #inch
            od_raised_face = 10.625 #inch
            d_hub_base = 9.6875 #inch
            bore = 7.98 #inch
            l_thru_hub = 4.0 #inch
            d_bevel_hub = 8.63 #inch
        else:
            print("Not implemented yet...")
            return None
    else:
        print("Not implemented yet...")
        return None

    return outside_diameter,thickness_min,od_raised_face,d_hub_base,bore,l_thru_hub,d_bevel_hub

if __name__=="__main__":

    material_flange=Material("SA-105","ASME")
    material_bolt = Material("SA-193-G7","ASME")
    material_flange.stress_yield = np.array([20000])
    material_flange.temperature_yield = np.array([50])
    flange = Flange("saber",material_flange,8,150,"RFWN")
