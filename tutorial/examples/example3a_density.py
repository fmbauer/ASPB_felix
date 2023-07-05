"""root system surface density"""
import sys; sys.path.append("../.."); sys.path.append("../../src/")

import plantbox as pb
import numpy as np

import matplotlib.pyplot as plt

path = "../../modelparameter/structural/plant/"
name = "P3_plant"  # "Crypsis_aculeata_Clausnitzer_1994"

rs = pb.RootSystem()
rs.readParameters(path + name + ".xml")

depth = 100
layers = 20
runs = 1

rl_ = []
for i in range(0, runs):
    rs.initialize(False)
    rs.simulate(60, False)
    ana = pb.SegmentAnalyser(rs)
    rl_.append(ana.distribution("length", 0., -depth, layers, True))

soilvolume = (depth / layers) * 10 * 10
rl_ = np.array(rl_) / soilvolume  # convert to density
rl_mean = np.mean(rl_, axis = 0)
rl_err = np.std(rl_, axis = 0) / np.sqrt(runs)

z_ = np.linspace(0, -depth, layers)  # z - axis
plt.plot(rl_mean, z_, "b")
plt.plot(rl_mean + rl_err, z_, "b:")
plt.plot(rl_mean - rl_err, z_, "b:")

plt.xlabel("root length density (cm$^3$ cm$^{-3}$)")
plt.ylabel("Depth (cm)")
# plt.legend(["mean value (" + str(runs) + " runs)", "error"])
plt.savefig("results/example_3a.png")
plt.show()
rs.write("results/rsml_brassica.rsml")
