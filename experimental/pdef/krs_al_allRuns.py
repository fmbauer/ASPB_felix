import sys;
sys.path.append("../.."); 
sys.path.append("../../src")
sys.path.append("../../src/python_modules")
import os 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from joblib import Parallel, delayed
from krs_al_1run import *


def do1Level(Plevel):
    krs_P0= np.array([])
    krshoot_P0 = np.array([])
    krplant_P0= np.array([])
    jc_P0  = np.array([])
    eswp_P0  =np.array([])
    eawp_P0  = np.array([])
    cwp_P0= np.array([])
    ti= np.array([])
    didDo = 0
    while didDo < runs:
        n_jobs_ = min( max(1,maxcore - 1),runs -  didDo)
        print(n_jobs_)
        tasks_iterator = (delayed(IamARun)
                                    (Plevel)
                                for i in range(n_jobs_))
        results = parallelizer(tasks_iterator)
        
        krs_P0 = np.concatenate((krs_P0, np.concatenate(([smalldic[0] for smalldic in results ]))))
        krshoot_P0 = np.concatenate((krshoot_P0, np.concatenate(([smalldic[1] for smalldic in results ]))))
        krplant_P0 = np.concatenate((krplant_P0, np.concatenate(([smalldic[2] for smalldic in results ]))))
        jc_P0 = np.concatenate((jc_P0, np.concatenate(([smalldic[3] for smalldic in results ]))))
        eswp_P0 = np.concatenate((eswp_P0, np.concatenate(([smalldic[4] for smalldic in results ]))))
        eawp_P0 = np.concatenate((eawp_P0, np.concatenate(([smalldic[5] for smalldic in results ]))))
        cwp_P0 = np.concatenate((cwp_P0, np.concatenate(([smalldic[6] for smalldic in results ]))))
        ti = np.concatenate((ti, np.concatenate(([smalldic[7] for smalldic in results ]))))
        
        ti1 = results[0][7]
        didDo += n_jobs_
    return krs_P0, krshoot_P0, krplant_P0, jc_P0, eswp_P0, eawp_P0 , cwp_P0, ti, ti1

def getFigdata(pdFinal, name, legend, ti):
    krs_final_mean = pdFinal.groupby('day').mean()
    krs_final_max = pdFinal.groupby('day').max()
    krs_final_min = pdFinal.groupby('day').min()
    krs_final_std = pdFinal.groupby('day').std()
    ti = ti
    krs_final_mean.to_csv(name+"Mean.csv")

    #print(krs_final_min)
    fig = plt.figure()
    plt.plot(ti, krs_final_mean.krs_P0,label = 'P0' )
    #plt.fill_between(ti, krs_final_min.krs_P0,krs_final_max.krs_P0, alpha = 0.1)
    plt.fill_between(ti, krs_final_mean.krs_P0 - krs_final_std.krs_P0 ,krs_final_mean.krs_P0 + krs_final_std.krs_P0, alpha = 0.1)

    plt.plot(ti, krs_final_mean.krs_P1,label = 'P1' )
    #plt.fill_between(ti, krs_final_min.krs_P1,krs_final_max.krs_P1, alpha = 0.1)
    plt.fill_between(ti, krs_final_mean.krs_P1 - krs_final_std.krs_P1 ,krs_final_mean.krs_P1 + krs_final_std.krs_P1, alpha = 0.1)

    plt.plot(ti, krs_final_mean.krs_P2,label = 'P2')
    #plt.fill_between(ti, krs_final_min.krs_P2,krs_final_max.krs_P2, alpha = 0.1)
    plt.fill_between(ti, krs_final_mean.krs_P2 - krs_final_std.krs_P2 ,krs_final_mean.krs_P2 + krs_final_std.krs_P2, alpha = 0.1)

    plt.plot(ti, krs_final_mean.krs_P3,label = 'P3')
    #plt.fill_between(ti, krs_final_mean.krs_P3 - krs_final_std.krs_P3 ,krs_final_mean.krs_P3 + krs_final_std.krs_P3, alpha = 0.1)
    plt.fill_between(ti, krs_final_min.krs_P3,krs_final_max.krs_P3, alpha = 0.1)
    plt.ylabel(legend)
    plt.xlabel('time (d)')
    # plt.ylim(0,0.004)
    plt.legend()
    #plt.show()
    fig.savefig(name+'.png', dpi=fig.dpi)


def getFigdataMaster(dataId):
    krs_final = pd.DataFrame({'day': resultP0[7], 'krs_P0': resultP0[dataId],'krs_P1': resultP1[dataId],'krs_P2': resultP2[dataId],'krs_P3': resultP3[dataId]})   
    krs_final.to_csv(namesFigs[dataId]+".csv")
    getFigdata(krs_final,namesFigs[dataId],legendsFigs[dataId], resultP0[8])
    


maxcore =  os.cpu_count()
runs =  max(1,maxcore - 1)
parallelizer = Parallel(n_jobs= max(1,maxcore - 1))

resultP0 = do1Level(0)
resultP1 = do1Level(1)
resultP2 = do1Level(2)
resultP3 = do1Level(3)
namesFigs = ["Krs","Krshoot", "Krplant", "jc","eswp","eawp","cwp"]
legendsFigs =[' Krs (cm$^2$ d$^{-1}$ )',  ' Krshoot (cm$^2$ d$^{-1}$ )',
              ' Krplant (cm$^2$ d$^{-1}$ )',  ' jc (cm$^3$ d$^{-1}$ )', 
              ' eswp (cm)',  ' eawp (cm)', ' cwp (cm)']

for dataid_ in range(len(namesFigs)):
    getFigdataMaster(dataid_)