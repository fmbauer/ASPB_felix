import sys;

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

import visualisation.vtk_plot as vp
import helpuqrMasterCopy1
import importlib
import pandas as pd

importlib.reload(helpuqrMasterCopy1)
from helpuqrMasterCopy1 import *
from helpuqrMasterCopy1 import setKrKx_xylem
# reload(helpuqrMasterCopy1)
import numpy as np

name = ''

def weather(simDuration, hp, condition):
    vgSoil = [0.01, 0.4193, 0.0051, 1.6727, 21.82]
    loam = [0.08, 0.43, 0.04, 1.6, 50]
    Qnigh = 0;
    Qday =960e-6 # 458*2.1 #960e-6   
    if (condition == "wet"):
        Tnigh = 15.8;
        Tday = 22
        # Tnigh = 13; Tday = 20.7
        # specificHumidity = 0.0097
        RHday = 0.6;
        RHnigh = 0.8
        Pair = 1010.00  # hPa
        thetaInit = 4 / 100  #40 / 100  # 15.59/100#
        cs = 350e-6
    elif condition == "dry":
        Tnigh = 20.7;
        Tday = 30.27
        # Tnigh = 15.34; Tday = 23.31
        # specificHumidity = 0.0097# 0.0111
        RHday = 0.3;
        RHnigh = 0.78
        Pair = 1070.00  # hPa
        thetaInit = 8 / 100  # 10.47/100#
        cs = 350e-6
    else:
        print("condition", condition)
        raise Exception("condition not recognised")
    coefhours =  1#max(0.,sinusoidal(simDuration) - 0.3) # total night 30% of the time
    RH_ = RHnigh + (RHday - RHnigh) * coefhours
    TairC_ = Tnigh + (Tday - Tnigh) * coefhours
    Q_ = Qnigh + (Qday - Qnigh) * coefhours
    # co2 paartial pressure at leaf surface (mol mol-1)
    # 390, 1231
    # RH = 0.5 # relative humidity
    es = 6.112 * np.exp((17.67 * TairC_) / (TairC_ + 243.5))
    ea = es * RH_  # qair2ea(specificHumidity,  Pair)
    assert ea < es
    # RH = ea/es
    assert ((RH_ > 0) and (RH_ < 1))
    bl_thickness = 1 / 1000  # m
    diffusivity = 2.5e-5  # m2/sfor 25°C
    rbl = bl_thickness / diffusivity  # s/m 13
    # cs = 350e-6
    Kcanopymean = 1e-1  # m2/s
    meanCanopyL = (2 / 3) * hp / 2
    rcanopy = meanCanopyL / Kcanopymean
    windSpeed = 2  # m/s
    zmzh = 2  # m
    karman = 0.41  # [-]

    rair = 1
    if hp > 0:
        rair = np.log((zmzh - (2 / 3) * hp) / (0.123 * hp)) * np.log(
            (zmzh - (2 / 3) * hp) / (0.1 * hp)) / (karman * karman * windSpeed)
        # print()
        # raise Exception

    pmean = theta2H(vgSoil, thetaInit)

    weatherVar = {'TairC': TairC_, 'TairK': TairC_ + 273.15, 'Pair': Pair, "es": es,
                  'Qlight': Q_, 'rbl': rbl, 'rcanopy': rcanopy, 'rair': rair, "ea": ea,
                  'cs': cs, 'RH': RH_, 'p_mean': pmean, 'vg': loam}
    # print("Env variables at", round(simDuration//1),"d",round((simDuration%1)*24),"hrs :\n", weatherVar)
    return weatherVar


def resistance2conductance(resistance, r, weatherX):
    resistance = resistance * (1 / 100)  # [s/m] * [m/cm] = [s/cm]
    resistance = resistance * r.R_ph * weatherX[
        "TairK"] / r.Patm  # [s/cm] * [K] * [hPa cm3 K−1 mmol−1] * [hPa] = [s] * [cm2 mmol−1]
    resistance = resistance * (1000) * (
                1 / 10000)  # [s cm2 mmol−1] * [mmol/mol] * [m2/cm2] = [s m2 mol−1]
    return 1 / resistance

runs = 10

for i in range(0,runs):

    def initPlant(simInit, condition):
        weatherInit = weather(simInit, 0, condition)
        simDuration = simInit # [day] init simtime
        # spellDuration = 5
        simMax = 28  # simStartSim+ spellDuration
        depth = 80
        dt = 1/24   # 10min
        verbose = True
        global name
        # plant system
        pl = pb.MappedPlant()  # pb.MappedRootSystem() #pb.MappedPlant()
        # pl2 = pb.MappedPlant(seednum = 2) #pb.MappedRootSystem() #pb.MappedPlant()
        # path = CPBdir + "/modelparameter/structural/plant/"
        name = "P0_plant"  # "Triticum_aestivum_adapted_2021"#
        pl.readParameters( name + ".xml")

        if name == 'P0_plant':

            for p in pl.getOrganRandomParameter(pb.leaf):
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
            for p in pl.getOrganRandomParameter(pb.stem):
                p.r = 0.758517633
                # p.lmax = (simMax-7)*0.758517633 
                # p.lmax=200
        if name == 'P1_plant':
            for p in pl.getOrganRandomParameter(pb.leaf):
                p.lb =  0 # length of leaf stem
                p.la,  p.lmax = 42.60617256, 42.60617256
                p.areaMax = 66.69532685  # cm2, area reached when length = lmax
                NLeaf = 100  # N is rather high for testing
                phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
                l = np.array([42.60617256,1 ,1, 0.3, 1, 42.60617256]) #distance from leaf center
                p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
                #p.tropismN = 5
                p.tropismS = 0.05
                p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
                p.createLeafRadialGeometry(phi, l, NLeaf)
            for p in pl.getOrganRandomParameter(pb.stem):
                r= 0.91546738
                p.r = r
                # p.lmax = (simMax-7)*0.91546738  
        if name == 'P2_plant':
            for p in pl.getOrganRandomParameter(pb.leaf):
                p.lb =  0 # length of leaf stem
                p.la,  p.lmax = 52.23664394, 52.23664394
                p.areaMax = 80.68274258  # cm2, area reached when length = lmax
                NLeaf = 100  # N is rather high for testing
                phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
                l = np.array([52.23664394,1 ,1, 0.3, 1, 52.23664394]) #distance from leaf center
                p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
                #p.tropismN = 5
                p.tropismS = 0.05
                p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
                p.createLeafRadialGeometry(phi, l, NLeaf)
            for p in pl.getOrganRandomParameter(pb.stem):
                r= 1.000613891
                p.r = r
                # p.lmax = (simMax-7)*1.000613891    

        if name == 'P3_plant':
            for p in pl.getOrganRandomParameter(pb.leaf):
                p.lb =  0 # length of leaf stem
                p.la,  p.lmax = 49.12433414, 49.12433414
                p.areaMax = 71.95670914  # cm2, area reached when length = lmax
                NLeaf = 100  # N is rather high for testing
                phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
                l = np.array([49.12433414,1 ,1, 0.3, 1, 49.12433414]) #distance from leaf center
                p.tropismT = 1 # 6: Anti-gravitropism to gravitropism
                p.tropismN = 5
                p.tropismS = 0.05
                p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
                p.createLeafRadialGeometry(phi, l, NLeaf)

            for p in pl.getOrganRandomParameter(pb.stem):
                r= 1.128705967
                p.r = r
                # p.lmax = (simMax-7)*1.128705967   


        # raise Exception
        sdf = pb.SDF_PlantBox(np.Inf, np.Inf, depth)

        pl.setGeometry(sdf)  # creates soil space to stop roots from growing out of the soil

        pl.initialize(verbose=True)  # , stochastic = False)
        
        parameters = pl.getOrganRandomParameter(pb.stem)
        for p in parameters:
            print(p)
        parameters = pl.getOrganRandomParameter(pb.root)
        for p in parameters:
            print(p)
        parameters = pl.getOrganRandomParameter(pb.leaf)
        for p in parameters:
            print(p)
        
        pl.simulate(simDuration, False)  # , "outputpm15.txt")
        print('SIMULATION')

        pLeaves = pl.getOrgans(4)
        totArea = 0
        area = []
        final_area = []
        final_length = []
        for pleaf in pLeaves:
            realized = False #(use theoretical length and not realized one)
            withPetiole = False #do not use petiole are to compute leaf area
            totArea += pleaf.leafArea(False, False) 
            banana = max(0., pleaf.getLength(False))*1.638117391
            area.append(banana)
            # print(area)
        final_area.append(np.sum(area))
        v = np.array(pl.getParameter('length'))
        final_length.append(np.sum(v))
        print('Area: ',final_area, 'length:', final_length)


        """ Coupling to soil """

        min_b = [-3. / 2, -12. / 2, -41.]  # distance between wheat plants
        max_b = [3. / 2, 12. / 2, 0.]
        rez = 0.5
        cell_number = [int(6 * rez), int(24 * rez), int(40 * rez)]  # 1cm3?
        layers = depth;
        soilvolume = (depth / layers) * 3 * 12
        k_soil = []
        initial = weatherInit["p_mean"]  # mean matric potential [cm] pressure head

        p_mean = initial
        p_bot = p_mean + depth / 2
        p_top = initial - depth / 2
        sx = np.linspace(p_top, p_bot, depth)
        picker = lambda x, y, z: max(int(np.floor(-z)), -1)
        sx_static_bu = sx
        pl.setSoilGrid(picker)  # maps segment

        """ Parameters phloem and photosynthesis """
        r = PhloemFluxPython(pl, psiXylInit=min(sx),
                            ciInit=weatherInit["cs"] * 0.5)  # XylemFluxPython(pl)#
        # r2 = PhloemFluxPython(#pl2,psiXylInit = min(sx),ciInit = weatherInit["cs"]*0.5) #XylemFluxPython(pl)#

        r = setKrKx_phloem(r)

        r.oldciEq = True

        
        r.g0 = 8e-3
        r.VcmaxrefChl1 = 1.1#1.28
        r.VcmaxrefChl2 = 4#8.33
        r.a1 = 0.6 / 0.4  # 0.7/0.3#0.6/0.4 #ci/(cs - ci) for ci = 0.6*cs
        r.a3 = 2
        r.alpha =0.4# 0.2#/2
        r.theta = 0.6#0.9#/2
        r.k_meso = 1e-3  # 1e-4
        r.setKrm2([[2e-5]])
        r.setKrm1([[10e-2]])  # ([[2.5e-2]])
        r.setRhoSucrose([[0.51], [0.65], [0.56]])  # 0.51
        # ([[14.4,9.0,0,14.4],[5.,5.],[15.]])
        rootFact = 2
        r.setRmax_st(
            [[2.4 * rootFact, 1.5 * rootFact, 0.6 * rootFact, 2.4 * rootFact], [2., 2.],
            [8.]])  # 6.0#*6 for roots, *1 for stem, *24/14*1.5 for leaves
        # r.setRmax_st([[12,9.0,6.0,12],[5.,5.],[15.]])
        r.KMrm = 0.1  # VERY IMPORTANT TO KEEP IT HIGH
        # r.exud_k = np.array([2.4e-4])#*10#*(1e-1)
        # r.k_gr = 1#0
        r.sameVolume_meso_st = False
        r.sameVolume_meso_seg = True
        r.withInitVal = True
        r.initValST = 0.  # 0.6#0.0
        r.initValMeso = 0.  # 0.9#0.0
        r.beta_loading = 0.6
        r.Vmaxloading = 0.05  # mmol/d, needed mean loading rate:  0.3788921068507634
        r.Mloading = 0.2
        r.Gr_Y = 0.8
        r.CSTimin = 0.4
        r.surfMeso = 0.0025
        r.leafGrowthZone = 2  # cm
        r.StemGrowthPerPhytomer = True  #
        r.psi_osmo_proto = -10000 * 1.0197  # schopfer2006
        r.fwr = 0

        r.cs = weatherInit["cs"]

        # r.r_forPhloem(24/14*1.5, 4)
        # r.r_forPhloem(24/14, 3)
        # r.r_forPhloem(6, 2) #because roots will have high C_ST less often
        r.expression = 6
        r.update_viscosity = True
        r.solver = 1
        r.atol = 1e-10
        r.rtol = 1e-6
        # r.doNewtonRaphson = False;r.doOldEq = False
        SPAD = 31.0
        chl_ = (0.114 * (SPAD ** 2) + 7.39 * SPAD + 10.6) / 10
        r.Chl = np.array([chl_])
        r.Csoil = 1e-4

        hp = max([tempnode[2] for tempnode in r.get_nodes()]) / 100

        weatherX = weather(simDuration, hp, condition = "wet")
        r.Patm = weatherX["Pair"]
        ##resistances
        r.g_bl = resistance2conductance(weatherX["rbl"], r, weatherX) / r.a2_bl
        r.g_canopy = resistance2conductance(weatherX["rcanopy"], r, weatherX) / r.a2_canopy
        r.g_air = resistance2conductance(weatherX["rair"], r, weatherX) / r.a2_air
        r.sh = 4e-4
        r.fwr = 0  # 0.001
        r.p_lcrit = -150
        #r.shmesophyll = 4e-4
        #r.fwrmesophyll = 0  # 0.001
        r.p_lcritmesophyll = -150
        r.gm = 0.01
        r.g0 = 8e-8
        r.alternativeAn = False
        r.limMaxErr = 1 / 100;

        r.Qlight = weatherX["Qlight"]  # ; TairC = weatherX["TairC"] ; text = "night"
        kr_l = 3.83e-5
        r = setKrKx_xylem(weatherX["TairC"], weatherX["RH"], r, kr_l)
        kr_l = 3.83e-5
        # r.setKr_meso([kr_l])
        r.es = weatherX["es"]
        return r, weatherX, sx


    #Q = np.arange(1e-6, 1000e-6, 100e-6)  # mol quanta m-2 s-1 light, example from leuning1995
    #TairC = np.arange(-10, 55, 5)
    #cs = np.arange(0e-6, 500e-6, 50e-6)  # mol mol-1
    simInit = 1
    simDuration = simInit
    maxSim = 28
    dt = 1/24 #in days
    rinit = initPlant(simDuration, condition="wet")
    weatherX = rinit[1]
    rC4 = rinit[0]

    rC4.PhotoType=pb.C4


    sx = rinit[2]  # np.linspace(-100, -20000, 100)
    p_errors = []

    kr_l = 3.83e-5
    rC4 = setKrKx_xylem(weatherX["TairC"], weatherX["RH"], rC4, kr_l)


    rC4.Patm = weatherX["Pair"]
    directoryN = "/fb_simOverTime/"


    AnC4 = []
    Antot =[]
    gc = []
    VjC4 = []
    VpC4 = []
    VcC4 = []
    RdC4 = []
    Rd_refC4 = []
    AnC4_mean = []
    FW_mean = []
    ci = []
    cs = []
    cics = []

    psixyl =[]
    j = 0
    while simDuration < maxSim:
        #update weather data
        hp = max([tempnode[2] for tempnode in rC4.get_nodes()]) / 100  # maxnode canopy [m]
        weatherX =  weather(simDuration, hp, condition = "dry")
        rC4.cs = weatherX["cs"]
        rC4.Qlight = weatherX["Qlight"]          
        rC4 = setKrKx_xylem(weatherX["TairC"], weatherX["RH"], rC4, kr_l)
        

        
        ##resistances
        rC4.g_bl = resistance2conductance(weatherX["rbl"], rC4, weatherX) / rC4.a2_bl
        rC4.g_canopy = resistance2conductance(weatherX["rcanopy"], rC4, weatherX) / rC4.a2_canopy
        rC4.g_air = resistance2conductance(weatherX["rair"], rC4, weatherX) / rC4.a2_air

        
        
        #
        # kr_l  = 3.83e-7
        # r.setKr_meso([kr_l])
        print("r.PhotoType, pb.C3, pb.C4",rC4.PhotoType,rC4.PhotoType)
        print("has",sum(rC4.plant.leafBladeSurface),"cm2 of leaf blade")
        print("has",np.sum(np.array(rC4.plant.getParameter('length'))),"cm root length")
        leaf_blade_area = sum(rC4.plant.leafBladeSurface)
        total_root_length = np.sum(np.array(rC4.plant.getParameter('length')))

        rC4.minLoop = 10000-10
        rC4.maxLoop = 10000
        rC4.solve_photosynthesis(sim_time_=simDuration, sxx_=sx, cells_=True,
                            ea_=weatherX["ea"], es_=weatherX["es"],
                            verbose_=False, doLog_=False, TairC_=weatherX["TairC"],
                            outputDir_="./results" + directoryN)
                            
        # print(np.mean(rC4.psiXyl))
        # psixyl.append(rC4.psiXyl)
        # ana = pb.SegmentAnalyser(rC4.plant.mappedSegments())
        # cutoff = 1e-15 #is get value too small, makes paraview crash
        # psiXyl_p = np.array(rC4.psiXyl)
        # psiXyl_p[abs(psiXyl_p) < cutoff] = 0
        # ana.addData("psi_Xyl",psiXyl_p)
        # ana.write("results"+directoryN+"photo_2_"+str(j)+".vtp") 



        idsC4 = np.where(np.array(rC4.ci)> 0)[0]
        if len(idsC4)>0:
            idsLeafBlade = np.where(np.array(rC4.plant.leafBladeSurface) >0)[0]
            print("for",name,'Antot:{},anmean:{} fw:{}, cics:{}'.format(
                   np.sum(np.array(rC4.Ag4Phloem)*12/(24*60*60)*10000/1000)* 1e6,
                   np.mean(np.array(rC4.An)[idsC4]) * 1e6,
                   np.mean(np.array(rC4.fw)[idsC4]),
                   np.mean(np.array(rC4.ci)[idsC4])/rC4.cs)) 
            Antot.append(np.sum(np.array(rC4.Ag4Phloem)*12/(24*60*60)*10000/1000)* 1e6)#  micromol CO2 m-2 s-1

            AnC4.append(np.array(rC4.An)[idsC4]*1e6)
            gc.append(np.mean(np.array(rC4.gco2)[idsC4]) * 1e6)

            AnC4_mean.append(np.mean(np.array(rC4.An)[idsC4]) * 1e6)
            FW_mean.append(np.mean(np.array(rC4.fw)[idsC4]))
            VjC4.append(np.mean(np.array(rC4.Vj)[idsC4])*1e6) 
            VpC4.append(np.mean(np.array(rC4.Vp)[idsC4])*1e6) 
            VcC4.append(np.mean(np.array(rC4.Vc)[idsC4])*1e6)
            RdC4.append(np.mean(np.array(rC4.Rd)[idsC4]) *1e6)
            Rd_refC4.append(np.mean(np.array(rC4.Rd_ref)[idsC4])*1e6) 
            ci.append(np.mean(np.array(rC4.ci)[idsC4])*1e6) 
            cics.append(np.mean(np.array(rC4.ci)[idsC4])/rC4.cs)
            
            print("did",rC4.loop,"loops")
            psiXyl_segment =np.array(rC4.psiXyl)[1:]
            organTypes = np.array(rC4.plant.organTypes)
            psiXyl_RootSegment = psiXyl_segment[np.where(organTypes == pb.root)]
            psiXyl_StemSegment = psiXyl_segment[np.where(organTypes ==  pb.stem)]
            psiXyl_LeafSegment = psiXyl_segment[np.where(organTypes ==  pb.leaf)] #at the beginning returns nan => no leaves
            print("RH",weatherX["ea"]/weatherX["es"])
            print("plant root",np.round(np.mean(psiXyl_RootSegment)),"stem",np.round(np.mean(psiXyl_StemSegment)),"leaf",np.round(np.mean(psiXyl_LeafSegment)))
            print("guard cell wat. pot.", rC4.gardCell_psi)
            print("mean soil water potential", np.mean(sx), "cm")
            raise Exception
            
        else:
            Antot.append(0.)

            AnC4.append(0.)
            gc.append(0.)

            AnC4_mean.append(0.)
            FW_mean.append(0.)
            VjC4.append(0.) 
            VpC4.append(0.) 
            VcC4.append(0.)
            RdC4.append(0.)
            Rd_refC4.append(0.) 
            ci.append(0.) 
            cics.append(0.) 
            
        

        
        rC4.plant.simulate(dt,  False)
        simDuration += dt
        j += 1
        # print(cs)
    #resultsAnC3 = pd.DataFrame(resultsAnC3)
    results = pd.DataFrame({'An_tot':Antot, 'gco2':gc,'An_mean':AnC4_mean, 'Fw_mean':FW_mean, 
                         'Vj': VjC4, 'Vp': VpC4, 'Vc':VcC4,'Rd':RdC4, 'Rd_ref':Rd_refC4,
                         'Ci': ci, 'cics':cics,
                         'blade': leaf_blade_area,'root_length':total_root_length})

    results.to_csv('results/'+str(i)+'_'+name+"_results.csv", index=False)




# print(AnC4)

# isInSoil = np.array([rC4.plant.seg2cell[si] >= 0 for si in range(len(rC4.plant.segments))])
# ana = pb.SegmentAnalyser(rC4.plant.mappedSegments())
# ana.addData("isInSoil", isInSoil)
# ana.write("fb_simOverTime.vtp", ["AnC4","organType", "subType", "isInSoil"]) 
