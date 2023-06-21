import numpy as np;
import sys;
sys.path.append("/mnt/c/Users/mobil/CPlantBox"); 
sys.path.append("/mnt/c/Users/mobil/CPlantBox/src/python_modules")
sys.path.append("/mnt/c/Users/mobil/CPlantBox/src")
import plantbox as pb
import visualisation.vtk_plot as vp


rs = pb.MappedRootSystem()
time_res = 2

time =28
# Open plant and root parameter from a file
# path = "/mnt/c/Users/mobil/CPlantBox_test_files/params/"
name = 'P3_plant'
rs.readParameters(name + ".xml")

for p in rs.getOrganRandomParameter(pb.leaf):
    p.lb =  0 # length of leaf stem
    p.la,  p.lmax = 49.12433414, 49.12433414
    p.areaMax = 71.95670914  # cm2, area reached when length = lmax
    N = 100  # N is rather high for testing
    phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
    l = np.array([49.12433414,1 ,1, 0.3, 1, 49.12433414]) #distance from leaf center
    p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
    p.tropismN = 5
    p.tropismS = 0.05
    p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
    p.createLeafRadialGeometry(phi, l, N)

for p in rs.getOrganRandomParameter(pb.stem):
    r= 1.128705967
    p.r = r
    p.lmax = (time-7)*r   



rs.initialize()
for t in range(0, (time * time_res) + 1):

    # Simulate
    rs.simulate(1.0 / time_res, True)
    # vp.plot_plant(rs, 'type')
    ana = pb.SegmentAnalyser(rs)
    ana.write("/mnt/c/Users/mobil/CPlantBox_test_files/results/timeline/P3" + "_" + str(t) + ".vtp") # e.g. 'subType'
# Simulate
rs.simulate(time)


# Plot, using vtk
# vp.plot_plant(rs, 'type')

# Export final result (as vtp)
rs.write("results/P3.vtp")
# rs.write('results/P0.rsml')
ana = pb.SegmentAnalyser(rs)

# # ana.mapPeriodic(15, 10)
ana.write("results/P3.vtp")


runs = 100
final_area = []
final_length = []

for i in range(0, runs):
    rs = pb.MappedPlant()
    rs.readParameters(name + ".xml")

    for p in rs.getOrganRandomParameter(pb.leaf):
        p.lb =  0 # length of leaf stem
        p.la,  p.lmax = 49.12433414, 49.12433414
        p.areaMax = 71.95670914  # cm2, area reached when length = lmax
        N = 100  # N is rather high for testing
        phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
        l = np.array([49.12433414,1 ,1, 0.3, 1, 49.12433414]) #distance from leaf center
        p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
        p.tropismN = 5
        p.tropismS = 0.05
        p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
    p.createLeafRadialGeometry(phi, l, N)

    for p in rs.getOrganRandomParameter(pb.stem):
        r= 1.128705967
        p.r = r
        p.lmax = (time-7)*r     

    rs.initialize(False)
    rs.simulate(time, False)
    vp.plot_plant(rs, 'type')

    v = np.array(rs.getParameter('length'))

    pLeaves = rs.getOrgans(4)
    totArea = 0
    area = []
    for pleaf in pLeaves:
        realized = False #(use theoretical length and not realized one)
        withPetiole = False #do not use petiole are to compute leaf area
        totArea += pleaf.leafArea(False, False) 
        banana = max(0., pleaf.getLength(False))*1.563152174
        area.append(banana)
     
    final_area.append(np.sum(area))
    
    final_length.append(np.sum(v))

print('mean', np.mean(final_area), 'std', np.std(final_area),'max', np.max(final_area), np.mean(final_length), np.std(final_length))
