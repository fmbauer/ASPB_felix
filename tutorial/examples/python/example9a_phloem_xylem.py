from fipy import *
from fipy.meshes.nonUniformGrid1D import NonUniformGrid1D as Grid1D
from fipy.meshes.nonUniformGrid2D import NonUniformGrid2D as Grid2D
from fipy.tools import numerix as np
import sys; sys.path.append("../../.."); sys.path.append("../../../src/python_modules")
from xylem_flux import XylemFluxPython  # Python hybrid solver
from phloem_flux import PhloemFluxPython
from CellVariablemod import CellVariablemod
import plantbox as pb
import vtk_plot as vp
import math
import os
from io import StringIO


home_dir = os.getcwd()
dir_name = "/results"
dir_name2 = home_dir + dir_name
test = os.listdir(dir_name2)
for item in test:
    if item.endswith("9a.txt"):
        os.remove(os.path.join(dir_name2, item))
    if item.endswith("9a.vtk"):
        os.remove(os.path.join(dir_name2, item))
    if item.endswith("9a.vtp"):
        os.remove(os.path.join(dir_name2, item))
        
        
np.set_printoptions(threshold=sys.maxsize)

class NullIO(StringIO):
    def write(self, txt):
       pass

######################
#
# plant
#
####################### 
pl = pb.MappedPlant() #pb.MappedRootSystem() #pb.MappedPlant()

path = "../../../modelparameter/plant/" #"../../../modelparameter/rootsystem/" 
name = "smallPlant_mgiraud"#"oneroot_mgiraud" #"manyleaves"# "oneroot" #"Anagallis_femina_Leitner_2010"  # Zea_mays_1_Leitner_2010
pl.readParameters(path + name + ".xml")
start =2. # 3.#1.275

""" Parameters xylem"""
kz = 4.32e-1  # axial conductivity [cm^3/day] 
kr = 1.728e-4  # radial conductivity of roots [1/day]
kr_stem = 1.e-20  # radial conductivity of stem  [1/day], set to almost 0
gmax = 0.004 #  cm3/day radial conductivity between xylem and guard cell
p_s = -200  # static water potential (saturation) 33kPa in cm
#p_g = -2000 # water potential of the guard cell
RH = 0.5 # relative humidity
TairC = 20
p_a =  -1000  #default outer water potential 
simtime = 15 # [day] for task b
k_soil = []
Q = 900e-6 # mol quanta m-2 s-1 light, example from leuning1995
cs = 350e-6 #co2 paartial pressure at leaf surface (mol mol-1)
TairK = TairC + 273.15


es = 0.61078 * math.exp(17.27 * TairC / (TairC + 237.3)) 
ea = es * RH 
VPD = es - ea 


""" Parameters phloem """
""" soil """
min_ = np.array([-50, -50, -150])
max_ = np.array([90, 40, 10])
res_ = np.array([5, 5, 5])
pl.setRectangularGrid(pb.Vector3d(min_), pb.Vector3d(max_), pb.Vector3d(res_), True)  # cut and map segments
pl.initialize()
pl.simulate(start, False)
phl = PhloemFluxPython(pl)
segs = pl.getPolylines() #segments regrouped per organ
phl.mp2mesh(segs) #creates grid
cellsIDOld = [phl.new2oldNodeID[xi] - 1 for xi in phl.mesh.cellFaceIDs[1] ]


######################

#tip indexes 
tiproots, tipstem, tipleaf = phl.get_organ_nodes_tips()
tiproots_newID = np.array([phl.old2newNodeID[xi] for xi in tiproots]).flatten()
tiproots=  [np.any([tiproots_newID == yi]) for yi in phl.mesh.faceVertexIDs[0]]
tiprootsfaces= sum([phl.mesh.faceVertexIDs[0] == xi for xi in tiproots_newID]) 
tiprootsfacesID= np.where(tiprootsfaces)[0]
tiprootscells= sum([phl.mesh.cellFaceIDs[1] == xi for xi in tiprootsfaces])
tiprootscellsID= np.where(tiprootscells)[0]

####
#
# Equations
#
####


cumulOutOld = CellVariable(mesh = phl.mesh, value=0.)
cumulGrOld = CellVariable(mesh = phl.mesh, value=0.)
cumulRmOld = CellVariable(mesh = phl.mesh, value=0.)
cumulAnOld = CellVariable(mesh = phl.mesh, value=0.)
dt =  0.9 * min(phl.mesh.length) ** 2 / (2 * 100) *2
phl.resetValues()    
phiOld = CellVariablemod(mesh = phl.mesh, value=0., hasOld = True)#180 * dt*0.1

cellVolumeOld = phl.mesh.cellVolumes

logfilermM = open('results/rmMax_9a.txt', "w")
logfilerm = open('results/rm_9a.txt', "w")
logfilephi = open('results/phi_9a.txt', "w")
logfilerg = open('results/rg_9a.txt', "w")
logfilergS = open('results/rgSink_9a.txt', "w")
logfileOut = open('results/outFow_9a.txt', "w")


phl.phi.updateOld()
growthSteps = []
issue = []
issueRes = []
issueLoop = []
phiConcentrationError = []


phl.cellsID = [phl.new2oldNodeID[xi] - 1 for xi in phl.mesh.cellFaceIDs[1] ]

print('IDs \n',  phl.mesh.cellFaceIDs)
print('IDs \n',  phl.cellsID)

steps = 5
timeSpanLeuning = 10 * 60 #time in seconds between to evaluatio of the gs operture/xylem flow
timeSinceLastLeuning = np.inf

for _ in range(steps):#TODO: add effect of gr on growth + add psi factor for growth
    print('step ', _, start + _ * dt, dt)

    print('len sum ', sum(phl.mesh.length) )
    #sys.stdout = NullIO()  
    ####
    #
    # plant growth
    #
    ####
    pl.simulate(dt , False)
    phl = PhloemFluxPython(pl)
    segs = pl.getPolylines() #segments regrouped per organ
    timeSinceLastLeuning += dt
    
    #if (timeSinceLastLeuning > timeSpanLeuning or cellVolumeOld != phl.mesh.cellVolumes ):
    ####
    #
    # xylem
    #
    ####
    
    nodes = phl.get_nodes()
    tiproots, tipstem, tipleaf = phl.get_organ_nodes_tips() #end node of end segment of each organ
    node_tips = np.concatenate((tiproots, tipstem, tipleaf))
    tiproots, tipstem, tipleaf = phl.get_organ_segments_tips() #end segment of each organ
    seg_tips = np.concatenate((tiproots, tipstem, tipleaf))


    phl.setKr([[kr],[kr_stem],[gmax]]) 
    phl.setKx([[kz]])
    phl.airPressure = p_a

    phl.seg_ind = seg_tips # segment indices for Neumann b.c.
    phl.node_ind = node_tips
    rx = phl.solve_leuning( sim_time = dt,sxx=[p_s], cells = True, Qlight = Q,VPD = VPD,
        Tl = TairK,p_linit = p_s,ci_init = cs,cs=cs, soil_k = [], log = False)
    fluxes = phl.radial_fluxes(dt, rx, [p_s], k_soil, True)  # cm3/day
        
        #timeSinceLastLeuning = 0
    phl.Px = rx
    
    ####
    #
    # phloem
    #
    ####
    
    phl.mp2mesh(segs) #creates grid
    phl.cellsID = [phl.new2oldNodeID[xi] - 1 for xi in phl.mesh.cellFaceIDs[1] ]
    
    if(len(phl.phi.value) > len(phiOld)): #place according to index ID
        CphiOld = phiOld * cellVolumeOld
        orderedCPhi = np.concatenate((np.array([x for _,x in sorted(zip(cellsIDOld, CphiOld))]), np.full(len(phl.phi.value)-len(phiOld),0.)))        
        orderedCPhiNew = np.take(orderedCPhi, phl.cellsID)/phl.mesh.cellVolumes
        growthSteps = np.append(growthSteps, [_])
        phl.phi = CellVariablemod(mesh = phl.mesh, value= orderedCPhiNew , hasOld =True)
        
        phl.phi.updateOld()
        
        orderedcumulOut = np.concatenate((np.array([x for _,x in sorted(zip(cellsIDOld, cumulOutOld))]), np.full(len(phl.phi.value)-len(phiOld),0.)))        
        orderedcumulOutNew = np.take(orderedcumulOut, phl.cellsID)        
        cumulOut = CellVariable(mesh = phl.mesh, value= orderedcumulOutNew)
        
        orderedcumulGr = np.concatenate((np.array([x for _,x in sorted(zip(cellsIDOld, cumulGrOld))]), np.full(len(phl.phi.value)-len(phiOld),0.)))        
        orderedcumulGrNew = np.take(orderedcumulGr, phl.cellsID)                
        cumulGr = CellVariable(mesh = phl.mesh, value= orderedcumulGrNew)
        
        orderedcumulRm = np.concatenate((np.array([x for _,x in sorted(zip(cellsIDOld, cumulRmOld))]), np.full(len(phl.phi.value)-len(phiOld),0.)))        
        orderedcumulRmNew = np.take(orderedcumulRm, phl.cellsID)                
        cumulRm = CellVariable(mesh = phl.mesh, value= orderedcumulRmNew)
        
        orderedcumulAn = np.concatenate((np.array([x for _,x in sorted(zip(cellsIDOld, cumulAnOld))]), np.full(len(phl.phi.value)-len(phiOld),0.)))        
        orderedcumulAnNew = np.take(orderedcumulAn, phl.cellsID)                
        cumulAn = CellVariable(mesh = phl.mesh, value= orderedcumulAnNew)
    
    else: 
        phl.phi = CellVariablemod(mesh = phl.mesh, value= phiOld.value * cellVolumeOld/phl.mesh.cellVolumes, hasOld =True)
        cumulOut = cumulOutOld
        cumulGr =cumulGrOld
        cumulRm = cumulRmOld
        cumulAn = cumulAnOld
        
    phl.resetValues()    
    
    eq = TransientTerm(var = phl.phi) == (phl.phi.faceValue * phl.phi.faceGrad*phl.intCoeff ).divergence\
        - phl.Rm   - phl.GrSink + phl.Source - phl.outFlow #add intcoef
    
    res = 1e+10
    resOld = 2e+10
    loop = 0
    
    #sys.stdout = sys.__stdout__
    #if update dt, do it here (after simulate)
    #because growth during simuate is for dt of the phloem model
    while res > max(1e-5, 1e-5* max(phl.phi)) and loop < 1000 and resOld != res:
        resOld = res
        res =  eq.sweep(dt= dt)
        loop += 1
        #print(res)
        #print(phl.phi.faceValue , phl.intCoeff)
    if res > max(1e-5, 1e-5 * max(phl.phi)) :
        print('no convergence! res: ', res)
        issue = np.append(issue, [_])
        issueRes = np.append(issueRes, [res])
        issueLoop = np.append(issueLoop, [loop])
    phl.phi.updateOld()
    cumulRm.setValue(cumulRm.value + phl.Rm.value * dt* phl.mesh.cellVolumes)
    cumulAn.setValue(cumulAn.value + phl.Source.value * dt* phl.mesh.cellVolumes)
    cumulGr.setValue(cumulGr.value + phl.GrSink.value * dt* phl.mesh.cellVolumes)
    cumulOut.setValue(cumulOut.value + phl.outFlow.value * dt* phl.mesh.cellVolumes)
    
    if _ % 100 == 0: #choose how often get output       
        ####
        #
        # copy of phi
        #
        ####
        
        reorderedPhi = np.array([x for _,x in sorted(zip(phl.cellsID,phl.phi.value))])
        reorderedOutFlow = np.array([x for _,x in sorted(zip(phl.cellsID,cumulOut))])
        reorderedRm = np.array([x for _,x in sorted(zip(phl.cellsID,cumulRm))])
        reorderedGrSink = np.array([x for _,x in sorted(zip(phl.cellsID,cumulGr))])
        orgNum = np.array([phl.newCell2organID[xi] for xi in phl.newCell2organID])
        reorderedorgNum = np.array([x for _,x in sorted(zip(phl.cellsID,orgNum))])
        ana = pb.SegmentAnalyser(phl.rs)
        ana.addData("phi",  np.around(reorderedPhi/phl.mesh.cellVolumes, 5))
        ana.addData("outFlow",  np.around(reorderedOutFlow/phl.mesh.cellVolumes, 5))
        ana.addData("Rm",  np.around(reorderedRm/phl.mesh.cellVolumes, 5))
        ana.addData("GrSink",  np.around(reorderedGrSink/phl.mesh.cellVolumes, 5))
        ana.addData("rx", phl.Px)
        ana.addData("fluxes", fluxes) 
        ana.addData("orgNr", reorderedorgNum) 
        ana.write("results/%s_example9a.vtp" %(_), ["radius", "surface", "phi", "outFlow", "Rm", "GrSink", "rx","fluxes","orgNr"])
        
        
        ####
        #
        # check balance
        #
        ####
        
        phimin = phl.phi * (phl.phi < 0 )
        print('sink priority check ',sum(phl.GrSink * (~phl.CSat)),sum(phl.outFlow*~phl.satisfaction)) #tip of stem negative at the beginning
        print('sucrose concentration < 0 at ',phl.phi[np.where(phl.phi < 0 )[0]],np.where(phl.phi < 0 )[0], ' sucrose vol. fraction > 0.65 at ',len(np.where(phl.VolFractSucrose > 0.65 )[0]))

        print('cumulated loading: ', sum(cumulAn), 'cumulated growth sink: ',sum(cumulGr), 'cumulated maintenance sink: ',sum(cumulRm), 'cumulated outflow: ',sum(cumulOut),'total C content in plant: ',sum(phl.phi* phl.mesh.cellVolumes))
        print('C_plant - C_Sink + C_source :',-sum(cumulAn) + sum(phl.phi* phl.mesh.cellVolumes) + sum(cumulGr)+ sum(cumulRm)+ sum(cumulOut))
        #print('check if value updates ',sum(phl.CSat), sum(phl.RmMax), sum(phl.Rm), sum(phl.Gr), sum(phl.GrSink), sum(phl.outFlow)) #check if value updates
        #print( 'Growth sink in segments with C limitation for maintenance (should be 0): ',) #check if value updates
        
        logfilephi.write('\n'+repr(phl.phi.value)[7:-2])
        logfilerm.write('\n'+repr(phl.Rm.value/phl.mesh.cellVolumes)[7:-2])
        logfilermM.write('\n'+repr(phl.RmMax.value/phl.mesh.cellVolumes)[7:-2])
        logfilergS.write('\n'+repr(phl.GrSink.value/phl.mesh.cellVolumes)[7:-2])
        logfilerg.write('\n'+repr(phl.Gr.value/phl.mesh.cellVolumes)[7:-2])
        logfileOut.write('\n'+repr(phl.outFlow.value/phl.mesh.cellVolumes)[7:-2])
        print('no convergence at step(s) ',issue, ' res: ', issueRes, ' loops ', issueLoop)
        print('phi value error at step(s) ',phiConcentrationError)
        #print('became bigger at step(s) ',growthSteps)
    
    #if(sum(abs(phl.GrSink * (~phl.CSat)))+sum(abs(phl.outFlow*~phl.satisfaction))\
    #    + sum(abs(phl.phi[np.where(phl.phi < 0 )[0]]))+sum(abs(phl.VolFractSucrose[np.where(phl.VolFractSucrose> 0.65 )[0]])) != 0):
     #   break
    #dt =  0.9 * min(phl.mesh.length) ** 2 / (2 * max(100,max((phl.phi.faceValue*phl.intCoeff).value)  ))
    phiOld = phl.phi.copy()
    cumulOutOld = cumulOut.copy()
    cumulGrOld = cumulGr.copy()
    cumulRmOld = cumulRm.copy()
    cumulAnOld = cumulAn.copy()
    cellVolumeOld = phl.mesh.cellVolumes
    cellsIDOld = phl.cellsID
    organGr = phl.organGr * dt
    print('growth per segment :',np.arange(len(organGr))/100 ,'\ndt :', dt)
    pl.setCWGr(np.arange(len(organGr))/100 ) #for testing
    #print('\nC konz > 0 ',len(np.where(phl.phi!=0)[0]), 'tot num seg ', len(phl.phi))
    #print(phl.phi,'\n', phl.phi.faceValue , '\n',phl.phi.faceGrad[2], '\n',phl.intCoeff)

logfilermM.close()
logfilerm.close()
logfilephi.close()
logfilerg.close()
logfilergS.close()
logfileOut.close()