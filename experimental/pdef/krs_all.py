import sys;
sys.path.append("../.."); 
sys.path.append("../../src")
sys.path.append("../../src/python_modules")

from functional.xylem_flux import XylemFluxPython  # Python hybrid solver
import plantbox as pb
import visualisation.vtk_plot as vp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



MaxSimtime = 28


""" Parameters """
def sinusoidal(t):
    return (np.sin(np.pi*t*2)+1)/2

# Environment

coefhours = sinusoidal(MaxSimtime)
Tmax = 24
Tmin = 18
TairC = Tmin + (Tmax - Tmin) * coefhours
hPa2cm = 1.0197
siPhi = (30 - TairC) / (91 + TairC)
siEnne=0
mu =  pow(10, (- 0.114 + (siPhi * (1.1 + 43.1 * pow(siEnne, 1.25) ))))
mu = mu /(24*60*60)/100/1000; #//mPa s to hPa d, 1.11837e-10 hPa d for pure water at 293.15K
mu = mu * hPa2cm #hPa d to cmh2o d
#g/ml
dEauPure = (999.83952 + TairC * (16.952577 + TairC *
        (- 0.0079905127 + TairC * (- 0.000046241757 + TairC *
        (0.00000010584601 + TairC * (- 0.00000000028103006)))))) /  (1 + 0.016887236 *
                                                                     TairC)/1000
molarMassWater = 18 #g/mol
mmol2cm3 = molarMassWater/dEauPure /1000#cm3/mmol
	# kr of tap root at age 0

a = 1.185 #mean stem radi from all P levels

kx_stem = (np.pi*(a*0.017)**4)/(8*mu)

kr_s = np.array([[0, 0], [1e4, 0]])
kz_s = np.array([[0, kx_stem], [1e4, kx_stem]])
kr_l_temp = 25

s2d = 1/3600/24 #[d/s]
MPa2cm = hPa2cm * 1000 #[cm/hPa * hPa/MPa]
m22cm2 = 10000 #cm2/m2


#25 mmol/m2/s/MPa
kr_l_temp2 = kr_l_temp*mmol2cm3 /m22cm2/s2d/MPa2cm #cm2/cm3/d
#too high
#m2/d
kr_l = np.array([[0, 3.83e-6 * hPa2cm], [1e4, 1000 * hPa2cm]])
kz_l = np.array([[0, kx_stem/10], [1e4, kx_stem/10]])

kr0 = kr_l
kz0 = kz_s
'''Artificial Shoot kx'''

# artificial shoot
kr0 = np.array([[0, 1.e-12], [1e4, 1.e-12]])
kz0 = np.array([[0, 1.], [1e4, 1.]])	

# kz0 = np.array([[0., 0.33355685296285653], [1.e-20, 0.33355685296285653]])		#
# kz0 = np.array([[0, 0.356832], [1e20, 0.356832]])		# kx of tap root at age 1e20

# tap root
# kr0 = np.array([[0, 1.14048e-3], [2, 1.08864e-3], [4, 1.0368e-3], [6, 9.8486e-4], [8, 9.3312e-4], [10, 8.8992e-4], [12, 8.47584e-4], [14, 8.06112e-4], [16, 7.67232e-4], [18, 7.3008e-4], [20, 6.9552e-4], [22, 6.61824e-4], [24, 6.29856e-4], [26, 5.99616e-4], [28, 5.7024e-4], [30, 5.42592e-4], [32, 5.16672e-4], [1e20, 5.16672e-4]])
# kz0 = np.array([[0, 0.067392], [2, 0.074736], [4, 0.082944], [6, 0.092448], [8, 0.101952], [10, 0.113184], [12, 0.126144], [14, 0.139968], [16, 0.154656], [18, 0.171936], [20, 0.190944], [22, 0.21168], [24, 0.235008], [26, 0.260928], [28, 0.28944], [30, 0.321408], [32, 0.356832], [1e20, 0.356832]])


'''Root conductivities with exponential growth'''
kr1 = np.array([[0.08243227637739019,0.0001063427809106925],[0.12403083800012145,0.00010600819000027001],[0.1658885823638555,0.0001062360127185785],[0.20800875944065764,0.000106033016896955],[0.2503946807170684,0.000106346827879547],[0.2930497207564021,0.00010642950047885449],[0.33597731881095994,0.0001062634438556405],[0.5104844350538453,0.00010638469493007],[0.6896456188450584,0.0001064569258243585],[0.8737159341936453,0.0001057606079808335],[1.2577145170642563,0.000113565939216522],[1.4582710891214414,0.0001142901954040455],[1.6649995920099006,4.00076833588706e-05],[1.8782919901321284,3.994978345837505e-05],[2.098578814953127,3.99623454358767e-05],[2.3263343967827597,3.9885567944048e-05],[2.562083014935793,4.0027559345494755e-05],[2.8064061667829177,3.676500658534805e-05],[3.0599512092164862,3.6763439236325344e-05],[4.494773247525064,3.890549566596665e-05],[8.838909102521768,4.10210723656745e-05],[24.94832020698389,4.29179747391326e-05]])
kz1 = np.array([[0.08243227637739019,0.001428701491936845],[0.12403083800012145,0.00141157523117865],[0.1658885823638555,0.00150353452632553],[0.20800875944065764,0.0014742021745241351],[0.2503946807170684,0.00137229824465936],[0.2930497207564021,0.001462688585623995],[0.33597731881095994,0.001406009043608815],[0.5104844350538453,0.0014675452059425699],[0.6896456188450584,0.0014077415905594049],[0.8737159341936453,0.0015130204053065551],[1.2577145170642563,0.00133612567641224],[1.4582710891214414,0.001350817954244865],[1.6649995920099006,0.0013481762863067248],[1.8782919901321284,0.001958719658258785],[2.3263343967827597,0.16138896628702398],[2.562083014935793,0.1633108719691035],[2.8064061667829177,0.1717536169909495],[3.0599512092164862,0.1736277194342965],[4.494773247525064,0.1617984411846205],[8.838909102521768,0.243831044057843],[24.94832020698389,0.33355685296285653]])

#seminal
kr4 =np.array([[0.112816849,0.000112594],[0.169748659,0.000112978],[0.227035186,0.000113248],[0.284680878,0.000112912],[0.342690268,0.000113171],[0.401067975,0.000113439],[0.459818704,0.000113637],[0.698649219,0.000121677],[0.943849293,0.00012169],[1.195768006,0.000122518],[1.454783947,0.00012298],[1.721308633,0.000122788],[1.995790444,0.000123039],[2.278719163,0.000123636],[2.570631231,0.0001233],[2.872115875,4.21906e-05],[3.183822263,4.2315e-05],[3.506467924,4.23972e-05],[3.840848695,4.24768e-05],[4.18785055,4.25832e-05],[6.151548613,3.92503e-05],[12.09693483,4.16085e-05],[34.14428184,4.30515e-05]])
kz4 = np.array([[0.11281684914998105,0.00104344808387714],[0.16974865860241395,0.001084251914759505],[0.2270351856664305,0.0010525523998907351],[0.2846808782552067,0.001103841878199095],[0.34269026847065615,0.00108312954572133],[0.40106797474159234,0.0010675539603493649],[0.4598187040302041,0.0010069550887520464],[0.6986492188960015,0.0009735756104467685],[0.9438492926240302,0.0009768755278932784],[1.1957680059275344,0.0009854992034376783],[1.4547839467929418,0.0009071226233668881],[1.7213086327468925,0.000865667148399697],[1.9957904441216752,0.0008010248002760815],[2.278719162705088,0.0008186655439126395],[2.570631231148137,0.000870364391740444],[2.8721158750002798,0.000843754941907991],[3.183822262929019,0.0008332761382412236],[3.5064679238316003,0.000911009348285576],[3.840848695261385,0.000875389202048173],[4.187850550141607,0.000898246121518689],[6.151548613165449,0.11215436059298149],[12.096934825678332,0.10148217370333051],[34.144281839931345,0.150518047844499]])

# l-type lateral
# kr2 = np.array([[0, 4.11264e-3], [1, 3.888e-3], [2, 3.672e-3], [3, 3.47328e-3], [4, 3.2832e-3], [5, 3.10176e-3], [6, 2.92896e-3], [7, 2.77344e-3], [8, 2.61792e-3], [9, 2.47968e-3], [10, 2.34144e-3], [11, 2.21184e-3], [12, 2.09952e-3], [13, 1.97856e-3], [14, 1.86624e-3], [15, 1.76256e-3], [16, 1.66752e-3], [17, 1.58112e-3], [1e20, 1.58112e-3]])
# kz2 = np.array([[0, 4.06944e-4], [1, 5.00256e-4], [2, 6.15168e-4], [3, 7.56e-4], [4, 9.3312e-4], [5, 1.14048e-3], [6, 1.40832e-3], [7, 1.728e-3], [8, 2.12544e-3], [9, 2.60928e-3], [10, 3.21408e-3], [11, 3.94848e-3], [12, 4.85568e-3], [13, 5.97024e-3], [14, 7.344e-3], [15, 8.9856e-3], [16, 0.0110592], [17, 0.0136512], [1e20, 0.0136512]])

kr2 = np.array([[0.17216300608705393,0.00011814790856374001],[0.26033859445570695,0.00011772680594141399],[0.34997169639406706,0.00011759868155066849],[0.44111130735821585,0.000118013417528984],[0.5338089356304391,0.00011772378367250949],[0.6281187771458294,0.0001178036806349285],[0.7240979057925947,0.000117636862682687],[1.125961665200367,0.000117637966391041],[1.560007591489408,0.00011792394054094201],[2.0318423759545428,3.7481355372504104e-05],[2.548678905856449,3.748182033219565e-05],[3.120015182978816,3.437261303083105e-05],[3.75871480095179,3.433395216767585e-05],[4.482812706744385,3.43365166096648e-05],[5.318722392441198,3.439823298059135e-05],[6.30739370680824,3.4359288049365e-05],[7.51742960190358,3.44139257267471e-05],[9.077437193392988,3.43931832083891e-05],[11.276144402855369,3.4370715979269455e-05],[15.03485920380716,3.4363613145709196e-05]])
kz2 = np.array([[0.17216300608705393,4.4768072266751145e-05],[0.26033859445570695,4.6349054075485354e-05],[0.34997169639406706,3.6227416994815655e-05],[0.44111130735821585,4.8713327058618e-05],[0.5338089356304391,3.9706371946602345e-05],[0.6281187771458294,4.2895381334739246e-05],[0.7240979057925947,4.65580350149153e-05],[1.125961665200367,4.22104082674339e-05],[1.560007591489408,3.8594389322433053e-05],[2.0318423759545428,4.2146643130030445e-05],[3.120015182978816,0.004316757905359855],[3.75871480095179,0.00431239331466016],[4.482812706744385,0.004323225988052145],[5.318722392441198,0.00430169788625176],[6.30739370680824,0.004345754295000255],[7.51742960190358,0.00434487892228969],[9.077437193392988,0.0043265316331582305],[11.276144402855369,0.004304888540330575],[15.03485920380716,0.0042966613356701655]])

# s-type lateral
# kr3 = np.array([[0, 4.11264e-3], [1, 3.888e-3], [2, 3.672e-3], [3, 3.47328e-3], [4, 3.2832e-3], [5, 3.10176e-3], [6, 2.92896e-3], [7, 2.77344e-3], [8, 2.61792e-3], [9, 2.47968e-3], [10, 2.34144e-3], [11, 2.21184e-3], [12, 2.09952e-3], [13, 1.97856e-3], [14, 1.86624e-3], [15, 1.76256e-3], [16, 1.66752e-3], [17, 1.58112e-3], [1e20, 1.58112e-3]])
# kz3 = np.array([[0, 4.06944e-4], [1, 5.00256e-4], [2, 6.15168e-4], [3, 7.56e-4], [4, 9.3312e-4], [5, 1.14048e-3], [6, 1.40832e-3], [7, 1.728e-3], [8, 2.12544e-3], [9, 2.60928e-3], [10, 3.21408e-3], [11, 3.94848e-3], [12, 4.85568e-3], [13, 5.97024e-3], [14, 7.344e-3], [15, 8.9856e-3], [16, 0.0110592], [17, 0.0136512], [1e20, 0.0136512]])

kr3 = np.array([[0.200254122123127,0.000129390622450947],[0.3039865472077396,0.000129699289462529],[0.41028052389123926,0.000129232506285035],[0.51926577126878,0.000129567186814999],[0.631082118606905,0.0001292076875711025],[0.7458805840656142,0.0001295009114293915],[0.8638246012425924,0.0001296203509850465],[1.3708437430993439,0.0001073382759855375],[1.9456546377424146,3.365280024629185e-05],[2.6092251168618796,3.379687849238945e-05],[3.3940624132730615,3.10777016348636e-05],[4.3546256324811665,3.110714184120505e-05],[5.5930070062437025,2.70109885520665e-05],[7.338407521862991,2.694561559503295e-05],[10.32218941124481,2.70282984028366e-05]])
kz3 = np.array([[0.200254122123127,1.4876873204742652e-05],[0.3039865472077396,1.60334194419736e-05],[0.41028052389123926,1.5787513976139952e-05],[0.8638246012425924,0.000776201512075445],[1.3708437430993439,0.0007679983531071785],[1.9456546377424146,0.0007745252668304815],[2.6092251168618796,0.0007652181272701905],[3.3940624132730615,0.0007729805938091705],[4.3546256324811665,0.0007682011183304045],[5.5930070062437025,0.0007532090253400926],[7.338407521862991,0.0007783360746834],[10.32218941124481,0.0007613256253168725]])

# shoot-born
kr5 = np.array([[0.08233900727871345,0.000133675979105574],[0.1238905016540107,0.000133826931499557],[0.16570088551454124,0.00013353191679336398],[0.207773405155146,0.000133533966573953],[0.25011136831553993,0.000134758249008305],[0.2927181457408428,0.0001344153385482685],[0.33559717279196777,0.00013528554438529348],[0.5099068406304184,0.0001350674852631835],[0.6888653101103879,0.0001405508737968255],[0.8727273566453477,0.00014100645240813547],[1.0617692914353087,0.0001421701293576315],[1.2562914591971874,0.00014259222363723702],[1.456621108845681,0.0001472611740842825],[1.663115706011982,0.00014806700032824903],[1.8761667716052333,0.00014844271074813552],[2.0962043499598675,0.0001395596875498485],[2.323702234698392,0.000144218683466018],[2.5591841119327503,5.28436517340678e-05],[2.803230821090675,5.2815110144092294e-05],[3.056488986603928,5.30836636709535e-05],[4.489687576378076,5.08139842681165e-05],[8.828908200914931,5.23839696968556e-05],[24.920092097298415,5.6739924599214845e-05]])
kz5 = np.array([[0.08233900727871345,0.0061012108489030895],[0.1238905016540107,0.0061287157563131],[0.16570088551454124,0.0061382740130904445],[0.207773405155146,0.00603781321781165],[0.25011136831553993,0.00631172718713725],[0.2927181457408428,0.005902104241609545],[0.33559717279196777,0.00596042829982248],[0.5099068406304184,0.0057859354283172106],[0.6888653101103879,0.00577029495359218],[0.8727273566453477,0.00669714417581805],[1.0617692914353087,0.007411225692761311],[1.2562914591971874,0.0069813721132007],[1.456621108845681,0.0063883507696567456],[1.663115706011982,0.006802020444944466],[1.8761667716052333,0.006945851992287625],[2.323702234698392,1.427732171171995],[2.5591841119327503,1.51687143593099],[2.803230821090675,1.60722277926901],[3.056488986603928,1.69169163420242],[4.489687576378076,2.34489158735256],[8.828908200914931,4.09461156681657],[24.920092097298415,6.608610426314295]])
# kr5 = kr1  
# kz5 = kz1

'''Root conductivities with linear growth from Adrien'''

kr1 = np.array([[0.227272727,0.000106343],[0.340909091,0.000106008],[0.454545455,0.000106236],[0.568181818,0.000106033],[0.681818182,0.000106347],[0.795454545,0.00010643],[0.909090909,0.000106263],[1.363636364,0.000106385],[1.818181818,0.000106457],[2.272727273,0.000105761],[3.181818182,0.000113566],[3.636363636,0.00011429],[4.090909091,4.00E-05],[4.545454545,3.99E-05],[5.,	4.00E-05],[5.454545455,3.99E-05],[5.909090909,4.00E-05],[6.363636364,3.68E-05],[6.818181818,3.68E-05],[9.090909091,3.89E-05],[13.63636364,4.10E-05],[18.18181818,4.29E-05]])

kr2= np.array([[0.3125,0.000112594],[0.46875,0.000112978],[0.625,0.000113248],[0.78125,0.000112912],[0.9375,0.000113171],[1.09375,0.000113439],[1.25,0.000113637],[1.875,0.000121677],[2.5,0.00012169],[3.125,	0.000122518],[3.75,0.00012298],[4.375,0.000122788],[5,0.000123039],[5.625,0.000123636],[6.25,0.0001233],[6.875,4.22E-05],[7.5,4.23E-05],[8.125,4.24E-05],[8.75,4.25E-05],[9.375,4.26E-05],[12.5,3.93E-05],[18.75,4.16E-05],[25,4.31E-05]])

kr3 = np.array([[2,0.000118148],[3,0.000117727],[4,0.000117599],[5,0.000118013],[6,0.000117724],[7,0.000117804],[8,0.000117637],[12,0.000117638],[16,0.000117924],[20,3.75E-05],[24,3.75E-05],[28,3.44E-05],[32,3.43E-05],[36,3.43E-05],[40,3.44E-05],[44,3.44E-05],[48,3.44E-05],[52,3.44E-05],[56,3.44E-05],[60,3.44E-05]])

kr4 = np.array([[3.649635036,0.000129391],[5.474452555,0.000129699],[7.299270073,0.000129233],[9.124087591,0.000129567],[10.94890511,0.000129208],[12.77372263,0.000129501],[14.59854015,0.00012962],[21.89781022,0.000107338],[29.19708029,3.37E-05],[36.49635036,3.38E-05],[43.79562044,3.11E-05],[51.09489051,3.11E-05],[58.39416058,2.70E-05],[65.69343066,2.69E-05],[72.99270073,2.70E-05]])

kr5 = np.array([[0.185185185,0.000133676],[0.277777778,0.000133827],[0.37037037,0.000133532],[0.462962963,0.000133534],[0.555555556,0.000134758],[0.648148148,0.000134415],[0.740740741,0.000135286],[1.111111111,0.000135067],[1.481481481,0.000140551],[1.851851852,0.000141006],[2.222222222,0.00014217],[2.592592593,0.000142592],[2.962962963,.000147261],[3.333333333,0.000148067],[3.703703704,0.000148443],[4.074074074,0.00013956],[4.444444444,0.000144219],[4.814814815,5.28E-05],[5.185185185,5.28E-05],[5.555555556,5.31E-05],[7.407407407,5.08E-05],[11.11111111,5.24E-05],[14.81481481,5.67E-05]])


kz1 = np.array([[0.227272727,0.001428701],[0.340909091,0.001411575],[0.454545455,0.001503535],[0.568181818,0.001474202],[0.681818182,0.001372298],[0.795454545,0.001462689],[0.909090909,0.001406009],[1.363636364,0.001467545],[1.818181818,0.001407742],[2.272727273,0.00151302],[3.181818182,0.001336126],[3.636363636,0.001350818],[4.090909091,0.001348176],[4.545454545,0.00195872],[5.454545455,0.161388966],[5.909090909,0.163310872],[6.363636364,0.171753617],[6.818181818,0.173627719],[9.090909091,0.161798441],[13.63636364,0.243831044],[18.18181818,0.333556853]])

kz2 = np.array([[0.3125,0.001043448],[0.46875,0.001084252],[0.625,0.001052552],[0.78125,0.001103842],[0.9375,0.00108313],[1.09375,0.001067554],[1.25,0.001006955],[1.875,0.000973576],[2.5,0.000976876],[3.125,0.000985499],[3.75,0.000907123],[4.375,0.000865667],[5,0.000801025],[5.625,0.000818666],[6.25,0.000870364],[6.875,0.000843755],[7.5,0.000833276],[8.125,0.000911009],[8.75,0.000875389],[9.375,0.000898246],[12.5,0.112154361],[18.75,0.101482174],[25,0.150518048]])

kz3 = np.array([[2,4.48E-05],[3,4.63E-05],[4,3.62E-05],[5,4.87E-05],[6,3.97E-05],[7,4.29E-05],[8,4.66E-05],[12,4.22E-05],[16,3.86E-05],[20,4.21E-05],[28,0.004316758],[32,0.004312393],[36,0.004323226],[40,0.004301698],[44,0.004345754],[48,0.004344879],[52,0.004326532],[56,0.004304889],[60,0.004296661]])

kz4 = np.array([[3.649635036,1.49E-05],[5.474452555,1.60E-05],[7.299270073,1.58E-05],[14.59854015,0.000776202],[21.89781022,0.000767998],[29.19708029,0.000774525],[36.49635036,0.000765218],[43.79562044,0.000772981],[51.09489051,0.000768201],[58.39416058,0.000753209],[65.69343066,0.000778336],[72.99270073,0.000761326]])

kz5 = np.array([[0.185185185,0.006101211],[0.277777778,0.006128716],[0.37037037,0.006138274],[0.462962963,0.006037813],[0.555555556,0.006311727],[0.648148148,0.005902104],[0.740740741,0.005960428],[1.111111111,0.005785935],[1.481481481,0.005770295],[1.851851852,0.006697144],[2.222222222,0.007411226],[2.592592593,0.006981372],[2.962962963,0.006388351],[3.333333333,0.00680202],[3.703703704,0.006945852],[4.444444444,1.427732171],[4.814814815,1.516871436],[5.185185185,1.607222779],[5.555555556,1.691691634],[7.407407407,2.344891587],[11.11111111,4.094611567],[14.81481481,6.608610426]])


#N = 4 # number of columns and rows
dist = 40  # distance between the root systems [cm]
dt = 1.
steps = round(MaxSimtime / dt)  # steps
runs = 10
krs_P0,krs_P1,krs_P2,krs_P3, count  = [], [],[], [],[]
krshoot_P0,krshoot_P1,krshoot_P2,krshoot_P3 = [], [],[], []
krplant_P0,krplant_P1,krplant_P2,krplant_P3 = [], [],[], []
jc_P0,jc_P1,jc_P2,jc_P3  = [], [],[], []
eswp_P0,eswp_P1,eswp_P2,eswp_P3  = [], [],[], []
eawp_P0,eawp_P1,eawp_P2,eawp_P3  = [], [],[], []
cwp_P0,cwp_P1,cwp_P2,cwp_P3  = [], [],[], []

for i in range(0,runs):

    allRS = []
    for i in range(0, 4):
        name = 'P'+str(i)+'_plant'
        rs = pb.MappedPlant()
        if name == 'P0_plant':
            for p in rs.getOrganRandomParameter(pb.leaf):
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
            for p in rs.getOrganRandomParameter(pb.stem):
                p.r = 0.758517633
                p.lmax = (MaxSimtime-7)*0.758517633 
        if name == 'P1_plant':
            for p in rs.getOrganRandomParameter(pb.leaf):
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
            for p in rs.getOrganRandomParameter(pb.stem):
                r= 0.91546738
                p.r = r
                p.lmax = (MaxSimtime-7)*0.91546738  
        if name == 'P2_plant':
            for p in rs.getOrganRandomParameter(pb.leaf):
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
            for p in rs.getOrganRandomParameter(pb.stem):
                r= 1.000613891
                p.r = r
                p.lmax = (MaxSimtime-7)*1.000613891    

        if name == 'P3_plant':
            for p in rs.getOrganRandomParameter(pb.leaf):
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

            for p in rs.getOrganRandomParameter(pb.stem):
                r= 1.128705967
                p.r = r
                p.lmax = (MaxSimtime-7)*1.128705967    


        # rs =  pb.MappedRootSystem()
        rs.setGeometry(pb.SDF_PlantBox(1.e6, 1.e6, 1.e6))  # not allowed to grow upwards out of soil
        p_s = np.linspace(-500, -2000, 30001)  #  -200.*np.ones((2001, 1))   # 3 meter down, from -200 to -500, resolution in mm
        # soil_index = lambda x, y, z: int(-10 * z)  # maps to p_s (hydrostatic equilibirum)
        soil_index = lambda x, y, z : 0
        p_s = -200  # static soil pressure [cm]
        p_a = -15000 #static air pressure
        rs.setSoilGrid(soil_index)
        print( name + ".xml")
        rs.readParameters( name + ".xml")
        # rs.getRootSystemParameter().seedPos = pb.Vector3d(dist * i,1, -3.)  # cm
        # rs.setSeed(2)
        rs.initialize()  
        allRS.append(rs)


    ö = 0
    for rs in allRS:
        ö +=1
        # kr5 = kr1  # shoot borne
        # kz5 = kz1

        krs_, krshoot_, krplant_, suf_, jc_, ti, eswp_,eawp_, cwp_ = [], [], [], [], [], [], [],[],[]
        k_soil = []
        simtime = 0
        r = XylemFluxPython(rs)
        r.setKrTables([[ kr1[:, 1], kr2[:, 1], kr3[:, 1], kr4[:, 1], kr5[:, 1]],[kr_s[:, 1],kr_s[:, 1]],[kr_l[:, 1]]],
                [[kr1[:, 0], kr2[:, 0], kr3[:, 0], kr4[:, 0], kr5[:, 0]],[kr_s[:, 0],kr_s[:, 0]],[kr_l[:, 0]]])
        r.setKxTables([[kz1[:, 1], kz2[:, 1], kz3[:, 1], kz4[:, 1], kz5[:, 1]],[kz_s[:, 1],kz_s[:, 1]],[kz_l[:, 1]]],
                [[kz1[:, 0], kz2[:, 0], kz3[:, 0], kz4[:, 0], kz5[:, 0]],[kz_s[:, 0],kz_s[:, 0]],[kz_l[:, 0]]])
        for j in range(steps):
            r.rs.simulate(dt, False)


            # roots = rs.getOrgans(2)
            # for root in roots:
                # if root.getParameter("subType") == 5:
                    # print(root.getNumberOfChildren())
            simtime += dt
            # vp.plot_roots(rs,'type')
            # vp.plot_plant(rs,'type')
            # shoot_segs = rs.getShootSegments()
            # print("Shoot segments", [str(s) for s in shoot_segs])
            #print("Shoot type", rs.subTypes[0])
            """ set up xylem parameters """
            

            r.airPressure = p_a
            
            # rx = r.solve_neumann(sim_time= simtime, value=0, sxx=[p_s], cells=True) #water matric pot given per segment
            
            # fluxes = r.radial_fluxes(simtime, rx, [p_s], k_soil, True)  # cm3/day
            #raise Exception()
            #print(fluxes)
            # r.test()
            # r.plot_conductivities()
            # r.find_base_segments()
            suf = r.get_suf(j)
            #print("Sum of SUF", np.sum(suf), "from", np.min(suf), "to", np.max(suf), "summed positive", np.sum(suf[suf >= 0]))
            suf_.append(suf)


            krs,krshoot,krplant, jc, eswp, eawp,cwp = r.get_krs(j, plant = True)
            print("P nr", ö,"simtime",int(simtime))
            print("\tkrs",np.around(krs,3),"krshoot",np.around(krshoot,3),"krplant",np.around(krplant,3))
            print("\tjc", np.around(jc,2), "eswp",np.around(eswp), "eawp",np.around(eawp),"cwp",np.around( cwp))
            print("\tsum of SUF",np.around( np.sum(suf),2), "summed positive",np.around( np.sum(suf[suf >= 0]),2) )
            # print("\tRx",np.around( rx,2), "rx")

            #print("Krs: ", krs)
            #print("time: ", j)
            krs_.append(krs/1000000/10000*3600/24*hPa2cm)
            # krs_.append(krs)
            krshoot_.append(krshoot)
            krplant_.append(krplant)
            jc_.append(jc)
            eswp_.append(eswp)
            eawp_.append(eawp)
            cwp_.append(cwp)
            ti.append(simtime)
            suf_.append(suf)
            
            # ana = pb.SegmentAnalyser(r.rs.mappedSegments())
            # ana.addData("RX", krs_)
            # ana.write("test"+str(j)+".vtp", ["rx","organType", "subType", "isInSoil"]) 

        """ Krs plot """
        if ö == 1:
            count.extend(ti)
            krs_P0.extend(krs_)
            krshoot_P0.extend(krshoot_)
            krplant_P0.extend(krplant_)
            jc_P0.extend(jc_)
            eswp_P0.extend(eswp_)
            eawp_P0.extend(eawp_)
            cwp_P0.extend(cwp_)
        elif ö == 2:
            krs_P1.extend(krs_)
            krshoot_P1.extend(krshoot_)
            krplant_P1.extend(krplant_)
            jc_P1.extend(jc_)
            eswp_P1.extend(eswp_)
            eawp_P1.extend(eawp_)
            cwp_P1.extend(cwp_)
        elif ö == 3:
            krs_P2.extend(krs_)
            krshoot_P2.extend(krshoot_)
            krplant_P2.extend(krplant_)
            jc_P2.extend(jc_)
            eswp_P2.extend(eswp_)
            eawp_P2.extend(eawp_)
            cwp_P2.extend(cwp_)
        elif ö == 4:
            krs_P3.extend(krs_)
            krshoot_P3.extend(krshoot_)
            krplant_P3.extend(krplant_)
            jc_P3.extend(jc_)
            eswp_P3.extend(eswp_)
            eawp_P3.extend(eawp_)
            cwp_P3.extend(cwp_)
            
def getFigdata(pdFinal, name, legend, ti):
    krs_final_mean = pdFinal.groupby('day').mean()
    krs_final_max = pdFinal.groupby('day').max()
    krs_final_min = pdFinal.groupby('day').min()
    krs_final_std = pdFinal.groupby('day').std()
    ti = ti

    #print(krs_final_min)
    fig = plt.figure()
    plt.plot(ti, krs_final_mean.krs_P0,label = 'P0' )
    # plt.fill_between(ti, krs_final_min.krs_P0,krs_final_max.krs_P0, alpha = 0.1)
    plt.fill_between(ti, krs_final_mean.krs_P0 - krs_final_std.krs_P0 ,krs_final_mean.krs_P0 + krs_final_std.krs_P0, alpha = 0.1)

    plt.plot(ti, krs_final_mean.krs_P1,label = 'P1' )
    # plt.fill_between(ti, krs_final_min.krs_P1,krs_final_max.krs_P1, alpha = 0.1)
    plt.fill_between(ti, krs_final_mean.krs_P1 - krs_final_std.krs_P1 ,krs_final_mean.krs_P1 + krs_final_std.krs_P1, alpha = 0.1)

    plt.plot(ti, krs_final_mean.krs_P2,label = 'P2')
    # plt.fill_between(ti, krs_final_min.krs_P2,krs_final_max.krs_P2, alpha = 0.1)
    plt.fill_between(ti, krs_final_mean.krs_P2 - krs_final_std.krs_P2 ,krs_final_mean.krs_P2 + krs_final_std.krs_P2, alpha = 0.1)

    plt.plot(ti, krs_final_mean.krs_P3,label = 'P3')
    plt.fill_between(ti, krs_final_mean.krs_P3 - krs_final_std.krs_P3 ,krs_final_mean.krs_P3 + krs_final_std.krs_P3, alpha = 0.1)
    # plt.fill_between(ti, krs_final_min.krs_P3,krs_final_max.krs_P3, alpha = 0.1)
    plt.ylabel(legend)
    plt.xlabel('time (d)')
    plt.xlim(0,29)
    plt.legend()
    plt.show()
    fig.savefig(name+'.png', dpi=fig.dpi)
   

krs_final = pd.DataFrame({'day': count, 'krs_P0': krs_P0,'krs_P1': krs_P1,'krs_P2': krs_P2,'krs_P3': krs_P3})   
getFigdata(krs_final,"Krs", ' Krs (cm$^2$ d$^{-1}$ )', ti)
krs_final = pd.DataFrame({'day': count, 'krs_P0': krshoot_P0,'krs_P1': krshoot_P1,'krs_P2': krshoot_P2,'krs_P3': krshoot_P3})   
getFigdata(krs_final,"Krshoot", ' Krshoot (cm$^2$ d$^{-1}$ )', ti)
krs_final = pd.DataFrame({'day': count, 'krs_P0': krplant_P0,'krs_P1': krplant_P1,'krs_P2': krplant_P2,'krs_P3': krplant_P3})   
getFigdata(krs_final,"Krplant", ' Krplant (cm$^2$ d$^{-1}$ )', ti)
jc_final = pd.DataFrame({'day': count, 'krs_P0': jc_P0,'krs_P1': jc_P1,'krs_P2': jc_P2,'krs_P3': jc_P3})   
getFigdata(jc_final,"jc", 'Transpiration (cm$^3$ d$^{-1}$ )', ti)
eswp_final = pd.DataFrame({'day': count, 'krs_P0': eswp_P0,'krs_P1': eswp_P1,'krs_P2': eswp_P2,'krs_P3': eswp_P3})   
getFigdata(eswp_final,"eswp", ' eswp (cm)', ti)
eawp_final = pd.DataFrame({'day': count, 'krs_P0': eawp_P0,'krs_P1': eawp_P1,'krs_P2': eawp_P2,'krs_P3': eawp_P3})   
getFigdata(eswp_final,"eawp", ' eawp (cm)', ti)
cwp_final = pd.DataFrame({'day': count, 'krs_P0': cwp_P0,'krs_P1': cwp_P1,'krs_P2': cwp_P2,'krs_P3': cwp_P3})   
getFigdata(cwp_final,"cwp", ' cwp (cm)', ti)