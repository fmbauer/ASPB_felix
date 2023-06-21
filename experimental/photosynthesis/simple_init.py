import sys;
sys.path.append("../.."); 
sys.path.append("../../src")
sys.path.append("../../src/python_modules")
import plantbox as pb
import visualisation.vtk_plot as vp


from functional.xylem_flux import XylemFluxPython  # Python hybrid solver
import plantbox as pb
import visualisation.vtk_plot as vp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

name = 'P0_plant'
plant = pb.MappedPlant()
rs = pb.MappedPlant()

MaxSimtime=28



plant.setGeometry(pb.SDF_PlantBox(1.e6, 1.e6, 1.e6))  # not allowed to grow upwards out of soil
p_s = np.linspace(-500, -2000, 30001)  #  -200.*np.ones((2001, 1))   # 3 meter down, from -200 to -500, resolution in mm
# soil_index = lambda x, y, z: int(-10 * z)  # maps to p_s (hydrostatic equilibirum)
soil_index = lambda x, y, z : 0
p_s = -200  # static soil pressure [cm]
p_a = -15000 #static air pressure
plant.setSoilGrid(soil_index)
print( name + ".xml")
plant.readParameters( name + ".xml")

for p in plant.getOrganRandomParameter(pb.leaf):
    p.la,  p.lmax = 38.41053981, 38.41053981
    p.areaMax = 54.45388021  # cm2, area reached when length = lmax
    NLeaf = 100  # N is rather high for testing
    phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi    
    l = np.array([38.41053981,1 ,1, 0.3, 1, 38.41053981]) #distance from leaf center
    p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
    #p.tropismN = 5
    p.tropismS = 0.05
    p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
    p.createLeafRadialGeometry(phi,l,NLeaf)
for p in plant.getOrganRandomParameter(pb.stem):
    p.lmax = (MaxSimtime-7)*0.758517633



# rs.getRootSystemParameter().seedPos = pb.Vector3d(dist * i,1, -3.)  # cm
# rs.setSeed(2)
plant.initialize()
plant.simulate(28, False)
vp.plot_plant(plant,'type')

# allRS = []
# for i in range(0, 4):
#     name = 'P'+str(i)+'_plant'
#     rs = pb.MappedPlant()
#     if name == 'P0_plant':
#         for p in rs.getOrganRandomParameter(pb.leaf):
#             p.la,  p.lmax = 38.41053981, 38.41053981
#             p.areaMax = 54.45388021  # cm2, area reached when length = lmax
#             NLeaf = 100  # N is rather high for testing
#             phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi    
#             l = np.array([38.41053981,1 ,1, 0.3, 1, 38.41053981]) #distance from leaf center
#             p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
#             #p.tropismN = 5
#             p.tropismS = 0.05
#             p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
#             p.createLeafRadialGeometry(phi,l,NLeaf)
#         for p in rs.getOrganRandomParameter(pb.stem):
#             p.r = 0.758517633
#             p.lmax = (MaxSimtime-7)*0.758517633 
#     if name == 'P1_plant':
#         for p in rs.getOrganRandomParameter(pb.leaf):
#             p.lb =  0 # length of leaf stem
#             p.la,  p.lmax = 42.60617256, 42.60617256
#             p.areaMax = 66.69532685  # cm2, area reached when length = lmax
#             NLeaf = 100  # N is rather high for testing
#             phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
#             l = np.array([42.60617256,1 ,1, 0.3, 1, 42.60617256]) #distance from leaf center
#             p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
#             #p.tropismN = 5
#             p.tropismS = 0.05
#             p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
#             p.createLeafRadialGeometry(phi, l, NLeaf)
#         for p in rs.getOrganRandomParameter(pb.stem):
#             r= 0.91546738
#             p.r = r
#             p.lmax = (MaxSimtime-7)*0.91546738  
#     if name == 'P2_plant':
#         for p in rs.getOrganRandomParameter(pb.leaf):
#             p.lb =  0 # length of leaf stem
#             p.la,  p.lmax = 52.23664394, 52.23664394
#             p.areaMax = 80.68274258  # cm2, area reached when length = lmax
#             NLeaf = 100  # N is rather high for testing
#             phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
#             l = np.array([52.23664394,1 ,1, 0.3, 1, 52.23664394]) #distance from leaf center
#             p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
#             #p.tropismN = 5
#             p.tropismS = 0.05
#             p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
#             p.createLeafRadialGeometry(phi, l, NLeaf)
#         for p in rs.getOrganRandomParameter(pb.stem):
#             r= 1.000613891
#             p.r = r
#             p.lmax = (MaxSimtime-7)*1.000613891    

#     if name == 'P3_plant':
#         for p in rs.getOrganRandomParameter(pb.leaf):
#             p.lb =  0 # length of leaf stem
#             p.la,  p.lmax = 49.12433414, 49.12433414
#             p.areaMax = 71.95670914  # cm2, area reached when length = lmax
#             NLeaf = 100  # N is rather high for testing
#             phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
#             l = np.array([49.12433414,1 ,1, 0.3, 1, 49.12433414]) #distance from leaf center
#             p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
#             p.tropismN = 5
#             p.tropismS = 0.05
#             p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
#             p.createLeafRadialGeometry(phi, l, NLeaf)

#         for p in rs.getOrganRandomParameter(pb.stem):
#             r= 1.128705967
#             p.r = r
#             p.lmax = (MaxSimtime-7)*1.128705967    


#     # rs =  pb.MappedRootSystem()
#     rs.setGeometry(pb.SDF_PlantBox(1.e6, 1.e6, 1.e6))  # not allowed to grow upwards out of soil
#     p_s = np.linspace(-500, -2000, 30001)  #  -200.*np.ones((2001, 1))   # 3 meter down, from -200 to -500, resolution in mm
#     # soil_index = lambda x, y, z: int(-10 * z)  # maps to p_s (hydrostatic equilibirum)
#     soil_index = lambda x, y, z : 0
#     p_s = -200  # static soil pressure [cm]
#     p_a = -15000 #static air pressure
#     rs.setSoilGrid(soil_index)
#     print( name + ".xml")
#     rs.readParameters( name + ".xml")
#     # rs.getRootSystemParameter().seedPos = pb.Vector3d(dist * i,1, -3.)  # cm
#     # rs.setSeed(2)
#     rs.initialize()
  
#     allRS.append(rs)
#     rs.simulate(28, False)

#     vp.plot_plant(plant,'type')
