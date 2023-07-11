""" water movement within the root (static soil) """

import os
main_dir=os.environ['PWD']#dir of the file
directoryN = "/"+os.path.basename(__file__)[:-3]+"/"
results_dir = main_dir +"/results"+directoryN

if not os.path.exists(results_dir):
    os.makedirs(results_dir)
else:
    test = os.listdir(results_dir)
    for item in test:
        try:
            os.remove(results_dir+item)
        except:
            pass
import sys
CPBdir = "../.."
sys.path.append(CPBdir + "/src");
sys.path.append(CPBdir);
sys.path.append("../../..");
sys.path.append("..");
sys.path.append(CPBdir + "/src/python_modules");
sys.path.append("../build-cmake/cpp/python_binding/")  # dumux python binding
sys.path.append("../../build-cmake/cpp/python_binding/")
sys.path.append("../modules/")  # python wrappers
sys.path.append("../../experimental/photosynthesis/")

from functional.phloem_flux import PhloemFluxPython  
import plantbox as pb
import math
import numpy as np
import visualisation.vtk_plot as vp
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('AGG') 
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
#from plotnine import *

simInit = 7
simDuration = simInit # [day] init simtime
simMax =simInit+21
depth = 60
dt = 1 #1d
verbose = True

# plant system 
pl = pb.MappedPlant(seednum = 2) #
name = 'P0_plant'

pl.readParameters(name + ".xml")

for p in pl.getOrganRandomParameter(pb.leaf):
    p.lb =  0 # length of leaf stem
    p.la,  p.lmax = 38.41053981, 38.41053981
    p.areaMax = 54.45388021  # cm2, area reached when length = lmax
    N = 100  # N is rather high for testing
    phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
    l = np.array([38.41053981,1 ,1, 0.3, 1, 38.41053981]) #distance from leaf center
    p.tropismT = 0 # 6: Anti-gravitropism to gravitropism
    p.tropismN = 5
    p.tropismS = 0.05
    p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
p.createLeafRadialGeometry(phi, l, N)

for p in pl.getOrganRandomParameter(pb.stem):
    r= 0.758517633
    p.r = r
    p.lmax = (28-7)*r   
    p.lb =  5
#raise Exception
sdf = pb.SDF_PlantBox(np.Inf, np.Inf, depth )

pl.setGeometry(sdf) # creates soil space to stop roots from growing out of the soil

ö=0
pl.initialize(verbose = True)#, stochastic = False)
Nt = int(simMax/dt)
for i in range(Nt):
    pl.simulate(dt, False)#, "outputpm15.txt")  
    ana = pb.SegmentAnalyser(pl.mappedSegments())
    
    ana.write("results"+directoryN+"photo_"+ str(ö) +".vtp", ["organType"]) 
    
      
    ö +=1
    
