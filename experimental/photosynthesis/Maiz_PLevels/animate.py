
import sys;

CPBdir = "../../.."
sys.path.append(CPBdir + "/src");
sys.path.append(CPBdir);
sys.path.append("../../..");
sys.path.append("..");
sys.path.append(CPBdir + "/src/python_modules");
sys.path.append("../build-cmake/cpp/python_binding/")  # dumux python binding
sys.path.append("../../build-cmake/cpp/python_binding/")
sys.path.append("../modules/")  # python wrappers
sys.path.append("../../experimental/photosynthesis/")
import plantbox as pb
import visualisation.vtk_plot as vp
import visualisation.vis_tools as cpbvis
import numpy as np
filename = "../../modelparameter/structural/plant/vis_example_plant_maize.xml"
filename = "P0_plant.xml"

output = "./results/vis_plant"
# create a plant
plant = pb.MappedPlant()
plant.readParameters(filename)

# if filename == 'P0_plant.xml':
#     for p in plant.getOrganRandomParameter(pb.leaf):
#         p.la,  p.lmax = 38.41053981, 38.41053981
#         p.areaMax = 54.45388021  # cm2, area reached when length = lmax
#         NLeaf = 100  # N is rather high for testing
#         phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi    
#         l = np.array([38.41053981,1 ,1, 0.3, 1, 38.41053981]) #distance from leaf center
#         p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
#         #p.tropismN = 5
#         p.tropismS = 0.05
#         p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
#         p.createLeafRadialGeometry(phi,l,NLeaf)
#     for p in plant.getOrganRandomParameter(pb.stem):
#         p.r = 0.758517633
#         p.lmax = (28-7)*0.758517633 
        
vis = pb.PlantVisualiser(plant)
# Initialize
plant.initialize()
vis.SetGeometryResolution(8)
vis.SetLeafResolution(30)

# Simulate

plant.simulate(28, True)

vp.plot_plant(plant,'type')


vis.ResetGeometry()
vis.ComputeGeometry()

# Write the geometry to file#
data = cpbvis.PolydataFromPlantGeometry(vis)
cpbvis.WritePolydataToFile(data, output + ".vtp")