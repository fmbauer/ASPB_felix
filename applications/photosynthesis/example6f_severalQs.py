""" water movement within the root (static soil) """
import sys; sys.path.append("../.."); sys.path.append("../../src/python_modules")
from xylem_flux import XylemFluxPython  # Python hybrid solver
from Leuning import Leuning
import plantbox as pb
import vtk_plot as vp
import math

import numpy as np
import matplotlib.pyplot as plt

def setKrKx_xylem(TairC): #inC
    #mg/cm3
    hPa2cm = 1.0197
    dEauPure = (999.83952 + TairC * (16.952577 + TairC * 
        (- 0.0079905127 + TairC * (- 0.000046241757 + TairC * 
        (0.00000010584601 + TairC * (- 0.00000000028103006)))))) /  (1 + 0.016887236 * TairC)
    siPhi = (30 - TairC) / (91 + TairC)
    siEnne=0
    mu =  pow(10, (- 0.114 + (siPhi * (1.1 + 43.1 * pow(siEnne, 1.25) )))) 
    mu = mu /(24*60*60)/100/1000; #//mPa s to hPa d, 1.11837e-10 hPa d for pure water at 293.15K
    mu = mu * hPa2cm #hPa d to cmh2o d 

    #number of vascular bundles
    VascBundle_leaf = 32
    VascBundle_stem = 52
    VascBundle_root = 1 #valid for all root type
            
    #radius of xylem type^4 * number per bundle
    rad_x_l_1   = (0.0015 **4) * 2; rad_x_l_2   = (0.0005 **4) * 2   
    rad_x_s_1   = (0.0017 **4) * 3; rad_x_s_2   = (0.0008 **4) * 1     
    rad_x_r0_1  = (0.0015 **4) * 4    
    rad_x_r12_1 = (0.00041**4) * 4; rad_x_r12_2 = (0.00087**4) * 1
    rad_x_r3_1  = (0.00068**4) * 1      

    # axial conductivity [cm^3/day]        
    kz_l  = VascBundle_leaf *(rad_x_l_1 + rad_x_l_2)    *np.pi /(mu * 8)  
    kz_s  = VascBundle_stem *(rad_x_s_1 + rad_x_s_2)    *np.pi /(mu * 8) 
    kz_r0 = VascBundle_root * rad_x_r0_1                *np.pi /(mu * 8)  
    kz_r1 = VascBundle_root *(rad_x_r12_1 + rad_x_r12_2)*np.pi /(mu * 8) 
    kz_r2 = VascBundle_root *(rad_x_r12_1 + rad_x_r12_2)*np.pi /(mu * 8)  
    kz_r3 = VascBundle_root * rad_x_r3_1                *np.pi /(mu * 8) # 4.32e-1

    #radial conductivity [1/day],
    kr_l  = 3.83e-4 * hPa2cm# init: 3.83e-4 cm/d/hPa
    kr_s  = 0#1.e-20  * hPa2cm # set to almost 0
    kr_r0 = 6.37e-5 * hPa2cm 
    kr_r1 = 7.9e-5  * hPa2cm 
    kr_r2 = 7.9e-5  * hPa2cm  
    kr_r3 = 6.8e-5  * hPa2cm 
    
    r.setKr([[kr_r0,kr_r1,kr_r2,kr_r3],[kr_s,kr_s ],[kr_l,kr_l,kr_l]]) 
    r.setKx([[kz_r0,kz_r1,kz_r2,kz_r3],[kz_s,kz_s ],[kr_l,kr_l,kz_l]])
    
    
    Rgaz=8.314 #J K-1 mol-1 = cm^3*MPa/K/mol
    rho_h2o = dEauPure/1000#g/cm3
    Mh2o = 18.05 #g/mol
    MPa2hPa = 10000
    hPa2cm = 1/0.9806806
    #log(-) * (cm^3*MPa/K/mol) * (K) *(g/cm3)/ (g/mol) * (hPa/MPa) * (cm/hPa) =  cm                      
    p_a = np.log(RH) * Rgaz * rho_h2o * (TairC + 273.15)/Mh2o * MPa2hPa * hPa2cm

    r.airPressure = p_a #*MPa2hPa #used only with xylem
""" Parameters """
kz = 4.32e-1  # axial conductivity [cm^3/day] 
kr = 1.728e-4  # radial conductivity of roots [1/day]
kr_stem = 1.e-20  # radial conductivity of stem  [1/day], set to almost 0
gmax = 0.004 #  cm3/day radial conductivity between xylem and guard cell
p_s = -200  # static water potential (saturation) 33kPa in cm
#p_g = -2000 # water potential of the guard cell
RH = 0.5 # relative humidity
TairC = 20
p_a =  -1000  #default outer water potential 
simtime = 14.0  # [day] for task b
k_soil = []
cs = 350e-6 #co2 paartial pressure at leaf surface (mol mol-1)
TairK = TairC + 273.15


es = 0.61078 * math.exp(17.27 * TairC / (TairC + 237.3)) 
ea = es * RH 
VPD = es - ea 

# root system 
pl = pb.MappedPlant() #pb.MappedRootSystem() #pb.MappedPlant()
path = "../../modelparameter/plant/" #"../../../modelparameter/rootsystem/" 
name = "Triticum_aestivum_adapted_2021"#"manyleaves" #"Anagallis_femina_Leitner_2010"  # Zea_mays_1_Leitner_2010
pl.readParameters(path + name + ".xml")

""" soil """
min_ = np.array([-5, -5, -15])
max_ = np.array([9, 4, 0])
res_ = np.array([5, 5, 5])
pl.setRectangularGrid(pb.Vector3d(min_), pb.Vector3d(max_), pb.Vector3d(res_), True)  # cut and map segments


pl.initialize()
pl.simulate(simtime/10, False)
pl.simulate(simtime/10, False) #test to see if works in case of several simulate


r = Leuning(pl) 
nodes = r.get_nodes()


QMax = 900e-6 # mol quanta m-2 s-1 light, example from leuning1995
QMin = 300e-6 
Qs = np.linspace( QMin,QMax, len(r.get_segments_index(4))) #PAR per segment

r.setKr([[kr],[kr_stem],[gmax]]) 
r.setKx([[kz]])
r.airPressure = p_a
setKrKx_xylem(TairC )
# Numerical solution 
rx = r.solve_leuning(sim_time = simtime,sxx=[p_s], cells = True, Qlight = Qs,VPD = VPD,
Tl = TairK,p_linit = p_s,ci_init = cs,cs=cs, soil_k = [], log = True, verbose = True)

fluxes = r.radial_fluxes(simtime, rx, [p_s], k_soil, True)  # cm3/day
#r.summarize_fluxes(fluxes, simtime, rx, [p_s], k_soil, True, show_matrices = False)

# plot results 
fig, ax = plt.subplots()
name = ["root", "stem", "leaf"]
color = ['tab:blue', 'tab:orange', 'tab:green']
for ndType in [2, 3, 4]:
    y = r.get_nodes_organ_type(ndType)#coordinates
    x = rx[r.get_nodes_index(ndType)]
    ax.scatter(x, y[:,2], c=color[ndType-2],  label=name[ndType-2],
               alpha=0.3, edgecolors='none')

ax.legend()
ax.grid(True)
plt.xlabel("Xylem pressure (cm)")
plt.ylabel("Depth (cm)")
plt.title("Xylem matric potential (cm)")
plt.show()


fig, ax = plt.subplots()
name = ["root", "stem", "leaf"]
color = ['tab:blue', 'tab:orange', 'tab:green']
for ndType in [2, 3, 4]:
    segIdx = r.get_segments_index(ndType)
    nodesy = segIdx + np.ones(segIdx.shape, dtype = np.int64)
    y = nodes[nodesy]#coordinates
    x = fluxes[segIdx]
    ax.scatter(x, y[:,2], c=color[ndType-2],  label=name[ndType-2],
               alpha=0.3, edgecolors='none')

ax.legend()
ax.grid(True)
plt.xlabel("Fluxes (cm3/day)")
plt.ylabel("Depth (cm)")
plt.title("water fluxes")
plt.show()

#Additional vtk plot
ana = pb.SegmentAnalyser(r.rs)
ana.addData("rx", rx)
ana.addData("fluxes",fluxes)  # cut off for vizualisation
ana.write("results/example_6f.vtp", ["radius", "surface", "rx", "fluxes"]) #
#vp.plot_roots(ana, "rx", "Xylem matric potential (cm)")  # "fluxes"
