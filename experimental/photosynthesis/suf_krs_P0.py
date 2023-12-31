import sys;
sys.path.append("../.."); 
sys.path.append("../../src")

from functional.xylem_flux import XylemFluxPython  # Python hybrid solver
from functional.phloem_flux import PhloemFluxPython 
import plantbox as pb
import visualisation.vtk_plot as vp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def setKrKx_xylem(TairC, RH,r): #inC
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
    betaXylX = 1#0.1      
    kz_l  = VascBundle_leaf *(rad_x_l_1 + rad_x_l_2)    *np.pi /(mu * 8)  * betaXylX
    kz_s  = VascBundle_stem *(rad_x_s_1 + rad_x_s_2)    *np.pi /(mu * 8) * betaXylX 
    kz_r0 = VascBundle_root * rad_x_r0_1                *np.pi /(mu * 8) * betaXylX  
    kz_r1 = VascBundle_root *(rad_x_r12_1 + rad_x_r12_2)*np.pi /(mu * 8)  * betaXylX
    kz_r2 = VascBundle_root *(rad_x_r12_1 + rad_x_r12_2)*np.pi /(mu * 8)  * betaXylX 
    kz_r3 = VascBundle_root * rad_x_r3_1                *np.pi /(mu * 8) * betaXylX

    #radial conductivity [1/day],0.00014 #
    betaXyl = 1#0.1#0.1
    kr_l  = 3.83e-3 * hPa2cm * betaXyl# init: 3.83e-5  3.83e-4 cm/d/hPa
    kr_s  = 0.#1.e-20  * hPa2cm # set to almost 0
    kr_r0 =6.37e-5 * hPa2cm * betaXyl
    kr_r1 =7.9e-5  * hPa2cm * betaXyl
    kr_r2 =7.9e-5  * hPa2cm * betaXyl
    kr_r3 =6.8e-5  * hPa2cm * betaXyl
    l_kr = 0.8 #cm
    r.setKr([[kr_r0,kr_r1,kr_r2,kr_r0],[kr_s,kr_s ],[kr_l]], kr_length_=l_kr) 
    r.setKx([[kz_r0,kz_r1,kz_r2,kz_r0],[kz_s,kz_s ],[kz_l]])
    
    
    Rgaz=8.314 #J K-1 mol-1 = cm^3*MPa/K/mol
    rho_h2o = dEauPure/1000#g/cm3
    Mh2o = 18.05 #g/mol
    MPa2hPa = 10000
    hPa2cm = 1/0.9806806
    #log(-) * (cm^3*MPa/K/mol) * (K) *(g/cm3)/ (g/mol) * (hPa/MPa) * (cm/hPa) =  cm                      
    #p_a = np.log(RH) * Rgaz * rho_h2o * (TairC + 273.15)/Mh2o * MPa2hPa * hPa2cm
    #done withint solve photosynthesis
    #r.psi_air = p_a #*MPa2hPa #used only with xylem
    return r
def weather(simDuration, hp):
        
        Qnigh = 0; Qday = 960e-6 #458*2.1
        Tnigh = 15.8; Tday = 22
        RHday = 0.6; RHnigh = 0.88
        Pair = 1010.00 #hPa
        
        cs = 350e-6

        coefhours = 1
        RH_ = RHnigh + (RHday - RHnigh) * coefhours
        TairC_ = Tnigh + (Tday - Tnigh) * coefhours
        Q_ = Qnigh + (Qday - Qnigh) * coefhours
         #co2 paartial pressure at leaf surface (mol mol-1)
        #390, 1231
        #RH = 0.5 # relative humidity
        es =  6.112 * np.exp((17.67 * TairC_)/(TairC_ + 243.5))
        ea = es*RH_#qair2ea(specificHumidity,  Pair)
        assert ea < es
        #RH = ea/es
        assert ((RH_ > 0) and(RH_ < 1))
        bl_thickness = 1/1000 #1mm * m_per_mm
        diffusivity= 2.5e-5#m2/sfor 25*C
        rbl =bl_thickness/diffusivity #s/m 13
        #cs = 350e-6
        Kcanopymean = 1e-1 # m2/s
        meanCanopyL = (2/3) * hp /2
        rcanopy = meanCanopyL/Kcanopymean
        windSpeed = 2 #m/s
        zmzh = 2 #m
        karman = 0.41 #[-]
        
        rair = 1
        if hp > 0:
            rair = np.log((zmzh - (2/3)*hp)/(0.123*hp)) * np.log((zmzh - (2/3)*hp)/(0.1*hp)) / (karman*karman*windSpeed)

        weatherVar = {'TairC' : TairC_,'TairK' : TairC_ + 273.15,'Pair':Pair,"es":es,
                        'Qlight': Q_,'rbl':rbl,'rcanopy':rcanopy,'rair':rair,"ea":ea,
                        'cs':cs, 'RH':RH_}
                        
        print("Env variables at", round(simDuration//1),"d",round((simDuration%1)*24),"hrs :\n", weatherVar)
        return weatherVar
def resistance2conductance(resistance,r):
    resistance = resistance* (1/100) #[s/m] * [m/cm] = [s/cm]
    resistance = resistance * r.R_ph * weatherX["TairK"] / r.Patm # [s/cm] * [K] * [hPa cm3 K−1 mmol−1] * [hPa] = [s] * [cm2 mmol−1]
    resistance = resistance * (1000) * (1/10000)# [s cm2 mmol−1] * [mmol/mol] * [m2/cm2] = [s m2 mol−1]
    return 1/resistance
""" Parameters """
# artificial shoot
simtime = 28  # [day] for task b
steps=28
""" root system """
rs = pb.MappedPlant()
rs.setGeometry(pb.SDF_PlantBox(1.e6, 1.e6, 1.e6))  # not allowed to grow upwards out of soil
p_s = np.linspace(-500, -200, 6001)  #  -200.*np.ones((2001, 1))   # 3 meter down, from -200 to -500, resolution in mm
soil_index = lambda x, y, z: max(int(-10 * z),-1)  # maps to p_s (hydrostatic equilibirum)
rs.setSoilGrid(soil_index) 



path = "../../modelparameter/structural/plant/"
# path = '/mnt/c/Users/mobil/CPlantBox/modelparameter/rootsystem/'
name = "Triticum_aestivum_adapted_2023"
#"P0_rs"  # "Glycine_max"  # "Anagallis_femina_Leitner_2010"  # Zea_mays_1_Leitner_2010
rs.readParameters(path + name + ".xml")
rs.setSeed(2)  # random


rs.initialize()
for step in range(steps):
    rs.simulate(1, False)
    rs.write("test"+str(step)+".vtp");

""" set up xylem parameters """
r = PhloemFluxPython(rs,psiXylInit = min(p_s),ciInit = 350e-6)

r.fwr = 0#0.1
r.sh = 4e-4
r.gm=0.025#4
SPAD= 41.0
chl_ = (0.114 *(SPAD**2)+ 7.39 *SPAD+ 10.6)/10
r.limMaxErr = 1/100
r.maxLoop = 3000
r.minLoop=100
   
hp = max([tempnode[2] for tempnode in r.get_nodes()]) /100 #maxnode canopy [m]
weatherX = weather(1,hp)
r.Patm = weatherX["Pair"]
##resistances
r.g_bl = resistance2conductance(weatherX["rbl"],r) / r.a2_bl
r.g_canopy = resistance2conductance(weatherX["rcanopy"],r) / r.a2_canopy
r.g_air = resistance2conductance(weatherX["rair"],r) / r.a2_air
#r.setKx([[4.32e-2 ],[5 ],[1.3]])
#r.setKr([[1.73e-4], [0],[3.83e-3]])
TairC = 25
es =  6.112 * np.exp((17.67 * TairC)/(TairC + 243.5))
ea = es*0.6
""" for debugging """
r.test()
r = setKrKx_xylem(TairC,ea/es,r)
r.solve_photosynthesis(sim_time_ = simtime, sxx_=p_s, cells_ = True,ea_ = ea,es_=es,
                    verbose_ = False, doLog_ = False,TairC_= TairC,outputDir_= "")
rx = np.array(r.psiXyl)
fluxes = np.array(r.outputFlux)
nodes = r.get_nodes()
                  
# plot results
if True:
    plt.plot(rx, nodes[:, 2] , "r*")
    plt.xlabel("Xylem pressure (cm)")
    plt.ylabel("Depth (cm)")
    plt.title("Xylem matric potential (cm)")
    plt.show()

    plt.plot(fluxes, nodes[1:, 2] , "r*")
    plt.xlabel("Fluxes")
    plt.ylabel("Depth (cm)")
    plt.title("water fluxes")
    plt.show()

print(r.gco2,r.Ev)
