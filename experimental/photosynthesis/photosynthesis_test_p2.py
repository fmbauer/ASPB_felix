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

import sys; 
sys.path.append("/mnt/c/Users/mobil/CPlantBox"); 
sys.path.append("/mnt/c/Users/mobil/CPlantBox/src/python_modules")
CPBdir = "/mnt/c/Users/mobil/CPlantBox"

from phloem_flux import PhloemFluxPython  
import plantbox as pb
import math
import numpy as np
import vtk_plot as vp
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('AGG') 
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
#from plotnine import *

#       qr, qs, alpha, n, ks (in [cm/d])
vgDi = [0.01, 0.445095720746729, 0.00644, 1.503, 1]
def theta2H(vg,theta):#(-) to cm
    thetar =vg[0]# 0.059
    thetas = vg[1]#0.445
    alpha = vg[2]#0.00644
    n = vg[3]#1.503
    nrev = 1/(1-1/n)
    H =-(((( (thetas - thetar)/(theta - thetar))**nrev) - 1)**(1/n))/alpha
    return(H)#cm

def sinusoidal(t):
    return (np.sin(np.pi*t*2)+1)/2

def qair2rh(qair, es_, press):
    e =qair * press / (0.378 * qair + 0.622)
    rh = e / es_
    rh=max(min(rh, 1.),0.)
    return rh


def weather(simDuration):
    vgSoil = [0.05, 0.45, 0.00644, 1.503, 1]
    Qmin = 0; Qmax = 960e-6 #458*2.1
    Tmin = 15.8; Tmax = 22
    specificHumidity = 0.0097
    Pair = 1010.00 #hPa
    thetaInit = 30/100

    coefhours = sinusoidal(simDuration)
    TairC_ = Tmin + (Tmax - Tmin) * coefhours
    Q_ = Qmin + (Qmax - Qmin) * coefhours
    cs = 850e-6 #co2 paartial pressure at leaf surface (mol mol-1)
    #RH = 0.5 # relative humidity
    es =  6.112 * np.exp((17.67 * TairC_)/(TairC_ + 243.5))
    RH = qair2rh(specificHumidity, es, Pair)
    
    pmean = theta2H(vgSoil, thetaInit)
    
    weatherVar = {'TairC' : TairC_,
                    'Qlight': Q_,
                    'cs':cs, 'RH':RH, 'p_mean':pmean, 'vg':vgSoil}
    print("Env variables at", round(simDuration//1),"d",round((simDuration%1)*24),"hrs :\n", weatherVar)
    return weatherVar

def div0(a, b, c):        
    return np.divide(a, b, out=np.full(len(a), c), where=b!=0)
    
def div0f(a, b, c):    
    if b != 0:
        return a/b
    else:
        return a/c
        
def write_file_array(name, data):
    name2 = 'results'+ directoryN+ name+ '.txt'
    with open(name2, 'a') as log:
        log.write(','.join([num for num in map(str, data)])  +'\n')

def write_file_float(name, data):
    name2 = 'results' + directoryN+  name+ '.txt'
    with open(name2, 'a') as log:
        log.write(repr( data)  +'\n')

def setKrKx_xylem(TairC, RH): #inC
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
    VascBundle_leaf = 48 #32 (Russel et al., 1985) 
    VascBundle_stem = 152 #52 (Legland et al.,2017)
    VascBundle_root = 1 #valid for all root type
            
    #radius of xylem type^4 * number per bundle
    rad_x_l_1   = (0.0015 **4) * 3; rad_x_l_2   = (0.0005 **4) * 2   
    rad_x_s_1   = (0.0017 **4) * 3; rad_x_s_2   = (0.0008 **4) * 1     
    # rad_x_r0_1  = (0.0015 **4) * 4    
    # rad_x_r12_1 = (0.00041**4) * 4; rad_x_r12_2 = (0.00087**4) * 1
    # rad_x_r3_1  = (0.00068**4) * 1      

    # axial conductivity [cm^3/day]        
    # kz_l  = VascBundle_leaf *(rad_x_l_1 + rad_x_l_2)    *np.pi /(mu * 8)  
    # kz_s  = VascBundle_stem *(rad_x_s_1 + rad_x_s_2)    *np.pi /(mu * 8) 
    kz_l  = list(np.linspace(VascBundle_leaf *(rad_x_l_1 + rad_x_l_2)*np.pi /(mu * 8), VascBundle_leaf *(rad_x_l_1 + rad_x_l_2)*np.pi /(mu * 8),5) )
    kz_s  = list(np.linspace(VascBundle_stem *(rad_x_s_1 + rad_x_s_2)*np.pi /(mu * 8),VascBundle_stem *(rad_x_s_1 + rad_x_s_2)*np.pi /(mu * 8),5) )
    # kz_r0 = VascBundle_root * rad_x_r0_1                *np.pi /(mu * 8)  
    # kz_r1 = VascBundle_root *(rad_x_r12_1 + rad_x_r12_2)*np.pi /(mu * 8) 
    # kz_r2 = VascBundle_root *(rad_x_r12_1 + rad_x_r12_2)*np.pi /(mu * 8)  
    # kz_r3 = VascBundle_root * rad_x_r3_1                *np.pi /(mu * 8) # 4.32e-1

    #radial conductivity [1/day],
    kr_l  = list(np.linspace(3.83e-4 * hPa2cm, 3.83e-4 * hPa2cm, 5))# init: 3.83e-4 cm/d/hPa
    # kr_s  = 0.#1.e-20  * hPa2cm # set to almost 0
    kr_s = list(np.zeros(5))
    # kr_r0 = 6.37e-5 * hPa2cm 
    # kr_r1 = 7.9e-5  * hPa2cm 
    # kr_r2 = 7.9e-5  * hPa2cm  
    # kr_r3 = 6.8e-5  * hPa2cm 
    # l_kr = 0.8 #cm

    # kr_r0 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_Tap.csv').k)
    # kr_age_r0 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_Tap.csv').age)
    # kr_r1 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_Basal.csv').k)
    # kr_age_r1 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_Basal.csv').age)
    # kr_r2 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_SBR.csv').k)
    # kr_age_r2 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_SBR.csv').age)
    # kr_r3 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_LAT_A.csv').k)
    # kr_age_r3 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_LAT_A.csv').age)
    # kr_r4 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_LAT.csv').k)
    # kr_age_r4 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kr/kr_LAT.csv').age)

    # kz_r0 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_Tap.csv').k)
    # kz_age_r0 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_Tap.csv').age)
    # kz_r1 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_Basal.csv').k)
    # kz_age_r1 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_Basal.csv').age)
    # kz_r2 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_SBR.csv').k)
    # kz_age_r2 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_SBR.csv').age)
    # kz_r3 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_LAT_A.csv').k)
    # kz_age_r3 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_LAT_A.csv').age)
    # kz_r4 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_LAT.csv').k)
    # kz_age_r4 = list(pd.read_csv('/mnt/c/Users/mobil/CPlantBox_test_files/kx/kx_LAT.csv').age)


    # # r.setKr([[[[kr_rt0,krt1 ],kr_r1,kr_r2,kr_r0,kr_r3,kr_r3],[kr_s,kr_s ],[kr_l]],[ages]]) 
    # r.setKrTables([[kr_r0,kr_r1,kr_r2,kr_r2,kr_r3,kr_r4],[kr_s,kr_s ],[kr_l]],[[kr_age_r0,kr_age_r1,kr_age_r2,kr_age_r2,kr_age_r3,kr_age_r4],[[0.0,1.,5.,10.,28.],[0.0,1.,5.,10.,28.]],[[0.0,1.,5.,10.,28.]]])
    # r.setKxTables([[kz_r0,kz_r1,kz_r2,kz_r2,kz_r3,kz_r4],[kz_s,kz_s ],[kz_l]],[[kz_age_r0,kz_age_r1,kz_age_r2,kz_age_r2,kz_age_r3,kz_age_r4],[[0.0,1.,5.,10.,28.],[0.0,1.,5.,10.,28.]],[[0.0,1.,5.,10.,28.]]])
 
    #primary
    kr1 = np.array([[0.08243227637739019,0.0001063427809106925],[0.12403083800012145,0.00010600819000027001],[0.1658885823638555,0.0001062360127185785],[0.20800875944065764,0.000106033016896955],[0.2503946807170684,0.000106346827879547],[0.2930497207564021,0.00010642950047885449],[0.33597731881095994,0.0001062634438556405],[0.5104844350538453,0.00010638469493007],[0.6896456188450584,0.0001064569258243585],[0.8737159341936453,0.0001057606079808335],[1.2577145170642563,0.000113565939216522],[1.4582710891214414,0.0001142901954040455],[1.6649995920099006,4.00076833588706e-05],[1.8782919901321284,3.994978345837505e-05],[2.098578814953127,3.99623454358767e-05],[2.3263343967827597,3.9885567944048e-05],[2.562083014935793,4.0027559345494755e-05],[2.8064061667829177,3.676500658534805e-05],[3.0599512092164862,3.6763439236325344e-05],[4.494773247525064,3.890549566596665e-05],[8.838909102521768,4.10210723656745e-05],[24.94832020698389,4.29179747391326e-05]])
    kz1 = np.array([[0.08243227637739019,0.001428701491936845],[0.12403083800012145,0.00141157523117865],[0.1658885823638555,0.00150353452632553],[0.20800875944065764,0.0014742021745241351],[0.2503946807170684,0.00137229824465936],[0.2930497207564021,0.001462688585623995],[0.33597731881095994,0.001406009043608815],[0.5104844350538453,0.0014675452059425699],[0.6896456188450584,0.0014077415905594049],[0.8737159341936453,0.0015130204053065551],[1.2577145170642563,0.00133612567641224],[1.4582710891214414,0.001350817954244865],[1.6649995920099006,0.0013481762863067248],[1.8782919901321284,0.001958719658258785],[2.3263343967827597,0.16138896628702398],[2.562083014935793,0.1633108719691035],[2.8064061667829177,0.1717536169909495],[3.0599512092164862,0.1736277194342965],[4.494773247525064,0.1617984411846205],[8.838909102521768,0.243831044057843],[24.94832020698389,0.33355685296285653]])

    #seminal
    kr4 =np.array([[0.112816849,0.000112594],[0.169748659,0.000112978],[0.227035186,0.000113248],[0.284680878,0.000112912],[0.342690268,0.000113171],[0.401067975,0.000113439],[0.459818704,0.000113637],[0.698649219,0.000121677],[0.943849293,0.00012169],[1.195768006,0.000122518],[1.454783947,0.00012298],[1.721308633,0.000122788],[1.995790444,0.000123039],[2.278719163,0.000123636],[2.570631231,0.0001233],[2.872115875,4.21906e-05],[3.183822263,4.2315e-05],[3.506467924,4.23972e-05],[3.840848695,4.24768e-05],[4.18785055,4.25832e-05],[6.151548613,3.92503e-05],[12.09693483,4.16085e-05],[34.14428184,4.30515e-05]])
    kz4 = np.array([[0.11281684914998105,0.00104344808387714],[0.16974865860241395,0.001084251914759505],[0.2270351856664305,0.0010525523998907351],[0.2846808782552067,0.001103841878199095],[0.34269026847065615,0.00108312954572133],[0.40106797474159234,0.0010675539603493649],[0.4598187040302041,0.0010069550887520464],[0.6986492188960015,0.0009735756104467685],[0.9438492926240302,0.0009768755278932784],[1.1957680059275344,0.0009854992034376783],[1.4547839467929418,0.0009071226233668881],[1.7213086327468925,0.000865667148399697],[1.9957904441216752,0.0008010248002760815],[2.278719162705088,0.0008186655439126395],[2.570631231148137,0.000870364391740444],[2.8721158750002798,0.000843754941907991],[3.183822262929019,0.0008332761382412236],[3.5064679238316003,0.000911009348285576],[3.840848695261385,0.000875389202048173],[4.187850550141607,0.000898246121518689],[6.151548613165449,0.11215436059298149],[12.096934825678332,0.10148217370333051],[34.144281839931345,0.150518047844499]])

    # l-type lateral
    kr2 = np.array([[0.17216300608705393,0.00011814790856374001],[0.26033859445570695,0.00011772680594141399],[0.34997169639406706,0.00011759868155066849],[0.44111130735821585,0.000118013417528984],[0.5338089356304391,0.00011772378367250949],[0.6281187771458294,0.0001178036806349285],[0.7240979057925947,0.000117636862682687],[1.125961665200367,0.000117637966391041],[1.560007591489408,0.00011792394054094201],[2.0318423759545428,3.7481355372504104e-05],[2.548678905856449,3.748182033219565e-05],[3.120015182978816,3.437261303083105e-05],[3.75871480095179,3.433395216767585e-05],[4.482812706744385,3.43365166096648e-05],[5.318722392441198,3.439823298059135e-05],[6.30739370680824,3.4359288049365e-05],[7.51742960190358,3.44139257267471e-05],[9.077437193392988,3.43931832083891e-05],[11.276144402855369,3.4370715979269455e-05],[15.03485920380716,3.4363613145709196e-05]])
    kz2 = np.array([[0.17216300608705393,4.4768072266751145e-05],[0.26033859445570695,4.6349054075485354e-05],[0.34997169639406706,3.6227416994815655e-05],[0.44111130735821585,4.8713327058618e-05],[0.5338089356304391,3.9706371946602345e-05],[0.6281187771458294,4.2895381334739246e-05],[0.7240979057925947,4.65580350149153e-05],[1.125961665200367,4.22104082674339e-05],[1.560007591489408,3.8594389322433053e-05],[2.0318423759545428,4.2146643130030445e-05],[3.120015182978816,0.004316757905359855],[3.75871480095179,0.00431239331466016],[4.482812706744385,0.004323225988052145],[5.318722392441198,0.00430169788625176],[6.30739370680824,0.004345754295000255],[7.51742960190358,0.00434487892228969],[9.077437193392988,0.0043265316331582305],[11.276144402855369,0.004304888540330575],[15.03485920380716,0.0042966613356701655]])

    # s-type lateral
    kr3 = np.array([[0.200254122123127,0.000129390622450947],[0.3039865472077396,0.000129699289462529],[0.41028052389123926,0.000129232506285035],[0.51926577126878,0.000129567186814999],[0.631082118606905,0.0001292076875711025],[0.7458805840656142,0.0001295009114293915],[0.8638246012425924,0.0001296203509850465],[1.3708437430993439,0.0001073382759855375],[1.9456546377424146,3.365280024629185e-05],[2.6092251168618796,3.379687849238945e-05],[3.3940624132730615,3.10777016348636e-05],[4.3546256324811665,3.110714184120505e-05],[5.5930070062437025,2.70109885520665e-05],[7.338407521862991,2.694561559503295e-05],[10.32218941124481,2.70282984028366e-05]])
    kz3 = np.array([[0.200254122123127,1.4876873204742652e-05],[0.3039865472077396,1.60334194419736e-05],[0.41028052389123926,1.5787513976139952e-05],[0.8638246012425924,0.000776201512075445],[1.3708437430993439,0.0007679983531071785],[1.9456546377424146,0.0007745252668304815],[2.6092251168618796,0.0007652181272701905],[3.3940624132730615,0.0007729805938091705],[4.3546256324811665,0.0007682011183304045],[5.5930070062437025,0.0007532090253400926],[7.338407521862991,0.0007783360746834],[10.32218941124481,0.0007613256253168725]])
    kr5 = kr1
    kz5 = kz1
    # r.setKr([[[[kr_rt0,krt1 ],kr_r1,kr_r2,kr_r0,kr_r3,kr_r3],[kr_s,kr_s ],[kr_l]],[ages]]) 
    r.setKrTables([[kr1[:, 1], kr2[:, 1], kr3[:, 1], kr4[:, 1], kr5[:, 1]],[kr_s,kr_s ],[kr_l]],[[kr1[:, 0], kr2[:, 0], kr3[:, 0], kr4[:, 0], kr5[:, 0]],[[0.0,1.,5.,10.,28.],[0.0,1.,5.,10.,28.]],[[0.0,1.,5.,10.,28.]]])
    r.setKxTables([[kz1[:, 1], kz2[:, 1], kz3[:, 1], kz4[:, 1], kz5[:, 1]],[kz_s,kz_s ],[kz_l]],[[kz1[:, 0], kz2[:, 0], kz3[:, 0], kz4[:, 0], kz5[:, 0]],[[0.0,1.,5.,10.,28.],[0.0,1.,5.,10.,28.]],[[0.0,1.,5.,10.,28.]]])
 
    
    Rgaz=8.314 #J K-1 mol-1 = cm^3*MPa/K/mol
    rho_h2o = dEauPure/1000#g/cm3
    Mh2o = 18.05 #g/mol
    MPa2hPa = 10000
    hPa2cm = 1/0.9806806
    #log(-) * (cm^3*MPa/K/mol) * (K) *(g/cm3)/ (g/mol) * (hPa/MPa) * (cm/hPa) =  cm                      
    p_a = np.log(RH) * Rgaz * rho_h2o * (TairC + 273.15)/Mh2o * MPa2hPa * hPa2cm

    r.psi_air = p_a #*MPa2hPa #used only with xylem

""" Parameters """

weatherInit = weather(0)
simInit = 7
simDuration = simInit # [day] init simtime
simMax =simInit+21
depth = 60
dt = 1/24 #1h
verbose = True

# plant system 
pl = pb.MappedPlant(seednum = 2) #pb.MappedRootSystem() #pb.MappedPlant()
# path = CPBdir+"/modelparameter/plant/"
path = "/mnt/c/Users/mobil/CPlantBox_test_files/params/"
name = 'P2_plant'
# name = "Triticum_aestivum_adapted_2021"#"wheat_uqr15" #"manyleaves"## "Anagallis_femina_Leitner_2010"  # Zea_mays_1_Leitner_2010

pl.readParameters(path + name + ".xml")

for p in pl.getOrganRandomParameter(pb.leaf):
    p.lb =  0 # length of leaf stem
    p.la,  p.lmax = 52.23664394, 52.23664394
    p.areaMax = 80.68274258  # cm2, area reached when length = lmax
    N = 100  # N is rather high for testing
    phi = np.array([-90,-80, -45, 0., 45, 90]) / 180. * np.pi
    l = np.array([52.23664394,1 ,1, 0.3, 1, 52.23664394]) #distance from leaf center
    p.tropismT = 0# 6: Anti-gravitropism to gravitropism
    p.tropismN = 5
    p.tropismS = 0.05
    p.tropismAge = 5 #< age at which tropism switch occures, only used if p.tropismT = 6
p.createLeafRadialGeometry(phi, l, N)

for p in pl.getOrganRandomParameter(pb.stem):
    r= 1.000613891
    p.r = r
    p.lmax = (28-7)*r   
    p.lb =  5
#raise Exception
sdf = pb.SDF_PlantBox(np.Inf, np.Inf, depth )

pl.setGeometry(sdf) # creates soil space to stop roots from growing out of the soil


pl.initialize(verbose = True)#, stochastic = False)
pl.simulate(simDuration, False)#, "outputpm15.txt")
ot_ =np.array(pl.organTypes)
segments_ = np.array(pl.segLength())
# vp.plot_plant(pl, 'type')

""" Coupling to soil """



min_b = [-3./2, -12./2, -61.]#distance between wheat plants
max_b = [3./2, 12./2, 0.]
cell_number = [6, 24, 61]#1cm3? 
layers = depth; soilvolume = (depth / layers) * 3 * 12
k_soil = []
initial = weatherInit["p_mean"]#mean matric potential [cm] pressure head

p_mean = -187
p_bot = p_mean + depth/2
p_top = p_mean - depth/2
sx = np.linspace(p_top, p_bot, depth)

#p_g = -2000 # water potential of the gua
picker = lambda x,y,z : max(int(np.floor(-z)),-1) #abovegroud nodes get index -1

#picker = lambda x, y, z: s.pick([x, y, z])    
pl.setSoilGrid(picker)  # maps segment


""" Parameters: photosynthesis """
#create object for photosynthesis and phloem
r = PhloemFluxPython(pl,psiXylInit = min(sx),ciInit = weatherInit["cs"]*0.5)

r.g0 = 8e-3 # minimal stomatal opening
r.VcmaxrefChl1 =1.28 #parameter for effect of N on assimilation
r.VcmaxrefChl2 = 8.33 #parameter for effect of N on assimilation
r.a1 = 0.5 #link An to g (kg1 in paper)
r.a3 = 1.5 #g_co2 to g_h2o (kg2 in paper)
r.alpha = 0.4   #influences Vj, alpha in paper
r.theta = 0.6   #influences Vj, omega in paper

r.cs = weatherInit["cs"] #external carbon concentration 
SPAD= 41.0
chl_ = (0.114 *(SPAD**2)+ 7.39 *SPAD+ 10.6)/10
r.Chl = np.array( [chl_]) #mean leaf chlorophyl content

""" for post processing """

ö=0
beginning = datetime.now()
AnSum = 0
results=[]
resultsAn=[]
resultsgco2=[]
resultsVc=[]
resultsVj=[]
resultscics=[]
resultsfw=[]
resultspl=[]



while simDuration < simMax: 
    
    print('simDuration:',simDuration )
    
    weatherX = weather(simDuration)

    r.Qlight = weatherX["Qlight"]
        
    #reset conductivity to water every time as depends on temperature    
    setKrKx_xylem(weatherX["TairC"], weatherX["RH"])
    
    #compute photosynthesis
    r.solve_photosynthesis(sim_time_ = simDuration, sxx_=sx, cells_ = True,RH_ = weatherX["RH"],
        verbose_ = False, doLog_ = False,TairC_= weatherX["TairC"] )
    
    #for post-processing: cummulative assimilated carbon
    AnSum += np.sum(r.Ag4Phloem)*dt
    organTypes = np.array(r.get_organ_types())#per node
    errLeuning = sum(r.outputFlux) #radial fluxes, should sum to 0
    fluxes = np.array(r.outputFlux)
    leavesSegs = np.where(organTypes==4)
    fluxes_leaves = fluxes[leavesSegs]
    if (min(r.Ev) < 0) or (min(r.Jw) < 0) or (min(fluxes_leaves)<0):
        print("leaf looses water", min(r.Ev),min(r.Jw), min(fluxes_leaves))
        raise Exception
    
    
    results.append(sum(np.where(organTypes == 4, fluxes,0))) #total leaf water exchange (transpiration)
    leafBlades = np.where(np.array(r.ci) > 0)[0]
    resultsAn.append(np.mean(np.array(r.An)[leafBlades])*1e6) #assimilation
    resultsVc.append(np.mean(np.array(r.Vc)[leafBlades])*1e6) #rate of carboxylation
    resultsVj.append(np.mean(np.array(r.Vj)[leafBlades])*1e6) #rate of photon flow
    resultsgco2.append(np.mean(np.array(r.gco2)[leafBlades])) # stomatal opening
    resultscics.append(np.mean(np.array(r.ci)[leafBlades])/r.cs) #ci/cs ratio
    resultsfw.append(np.mean(np.array(r.fw)[leafBlades])) #water scarcity factor for stomatal opening
    resultspl.append(np.mean(np.array(r.psiXyl)[leafBlades])) #leaf water potential
    
    """ soil water flow """   
    #in this example, we have a static soil
    fluxesSoil = r.soilFluxes(simDuration, r.psiXyl, sx, approx=False)
    #s.setSource(fluxesSoil.copy())  # richards.py 
    #s.solve(dt)
    #sx = s.getSolutionHead()  # richards.py    
    #min_sx, min_rx, max_sx, max_rx = np.min(sx), np.min(r.psiXyl), np.max(sx), np.max(r.psiXyl)
    #n = round((simDuration- simInit)/(simMax-simInit) * 100.)
    #print("[" + ''.join(["*"]) * n + ''.join([" "]) * (100 - n) + "], [{:g}, {:g}] cm soil [{:g}, {:g}] cm root at {:g} days {:g}"
     #       .format(min_sx, max_sx, min_rx, max_rx, s.simTime, r.psiXyl[0]))
          
                         
      
    """ for post processing """
    
    
    if verbose :
        print("\n\n\n\t\tat ", int(np.floor(simDuration)),"d", int((simDuration%1)*24),"h",  round(r.Qlight *1e6),"mumol m-2 s-1")
        print("Error in photos:\n\tabs (cm3/day) {:5.2e}".format(errLeuning))
    """ paraview output """    
    ana = pb.SegmentAnalyser(r.plant.mappedSegments())
    
    cutoff = 1e-15 #is get value too small, makes paraview crash
    fluxes_p = fluxes
    fluxes_p[abs(fluxes_p) < cutoff] = 0
    
    psiXyl_p = np.array(r.psiXyl)
    psiXyl_p[abs(psiXyl_p) < cutoff] = 0
    ana.addData("fluxes", fluxes_p)
    ana.addData("psi_Xyl",psiXyl_p)
    ana.write("results"+directoryN+"photo_"+ str(ö) +".vtp", ["fluxes","psi_Xyl"]) 
    
      
    ö +=1
    
    
    """ print to files """    
    write_file_array("fluxes", fluxes)
    write_file_array("psiXyl", r.psiXyl)
    
    verbose_simulate = False
    r.plant.simulate(dt, verbose_simulate)#, "outputpm15.txt") #time span in days /(60*60*24)
    
        
    
    simDuration += dt


timePlot = simInit + np.array(list(range(ö))) *dt
plotResults = True
if plotResults:
    fig, axs = plt.subplots(2,2)
    axs[0, 0].plot(timePlot, resultsAn) #assimilation
    axs[0, 0].set(xlabel='', ylabel='mean An (μmol CO2 m-2 s-1)')
    axs[0, 0].xaxis.set_major_locator(MaxNLocator(5))
    axs[1, 0].plot(timePlot, resultsVc, 'tab:red') #rate of carboxylation
    axs[1, 0].set(xlabel='time', ylabel='mean Vc (μmol CO2 m-2 s-1)')
    axs[1, 0].xaxis.set_major_locator(MaxNLocator(5))
    axs[0, 1].plot(timePlot, resultsVj, 'tab:brown') #rate of photon flow
    axs[0, 1].set(xlabel='', ylabel='mean Vj (μmol CO2 m-2 s-1)')
    axs[0, 1].xaxis.set_major_locator(MaxNLocator(5))
    axs[1, 1].plot(timePlot, resultsgco2, 'tab:brown') # stomatal opening
    axs[1, 1].set(xlabel='time', ylabel='mean gco2 (mol CO2 m-2 s-1)')
    axs[1, 1].xaxis.set_major_locator(MaxNLocator(5))
    plt.tight_layout()
    # plt.show()
    plt.savefig('results'+ directoryN+ 'fig1'+ '.png')
    fig, axs = plt.subplots(2,2)
    axs[0, 0].plot(timePlot, results) #total leaf water exchange (transpiration)
    print(list(timePlot),results)

    transpiration = pd.DataFrame({'time':timePlot, 'P0': results}) 
    transpiration.to_csv('results'+ directoryN+ 'transpiration'+ '.csv')
    
    axs[0, 0].set(xlabel='', ylabel='E')
    axs[0, 0].xaxis.set_major_locator(MaxNLocator(5))
    axs[0, 1].plot(timePlot, resultsfw, 'tab:brown') #water scarcity factor for stomatal opening
    axs[0, 1].set(xlabel='', ylabel='fw')
    axs[0, 1].xaxis.set_major_locator(MaxNLocator(5))
    axs[1, 0].plot(timePlot, resultspl, 'tab:brown') #leaf water potential
    axs[1, 0].set(xlabel='time', ylabel='pl')
    axs[1, 0].xaxis.set_major_locator(MaxNLocator(5))
    axs[1, 1].plot(timePlot, resultscics, 'tab:brown') #ci/cs ratio
    axs[1, 1].set(xlabel='time', ylabel='ci/cs (-)') 
    axs[1, 1].xaxis.set_major_locator(MaxNLocator(5))
    plt.tight_layout()
    # plt.show()
    plt.savefig('results'+ directoryN+ 'fig2'+ '.png')
    res = pd.DataFrame({'time':timePlot, 'P2_E': results, 'P2_fw': resultsfw, 'P2_pl':resultspl, 'P2_An':resultsAn, 'P2_Vc':resultsVc,'P2_Vj':resultsVj, 'P2_gco2': resultsgco2}) 
    res.to_csv('results'+ directoryN+ 'data'+ '.csv', index = False)
    
print("simDuration", simDuration, "d")

end = datetime.now()
print(end - beginning)