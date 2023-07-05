"""root system length over time"""
import sys; sys.path.append("../.."); sys.path.append("../../src/")

import plantbox as pb

import numpy as np
import matplotlib.pyplot as plt

path = "../../modelparameter/structural/plant/"
name = "P3_plant"

rs = pb.RootSystem()
rs.readParameters(path + name + ".xml")
rs.initialize()

simtime = 60.  # days
dt = 1.
N = round(simtime / dt)  # steps

# Plot some scalar value over time
stype = "length"
v_, v1_, v2_, v3_, v4_,v5_ = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
for i in range(0, N):
    rs.simulate(dt)
    t = np.array(rs.getParameter("type"))
    v = np.array(rs.getParameter(stype))
    v_[i] = np.sum(v)
    v1_[i] = np.sum(v[t == 1])
    v2_[i] = np.sum(v[t == 2])
    v3_[i] = np.sum(v[t == 3])
    v4_[i] = np.sum(v[t == 4])
t_ = np.linspace(dt, N * dt, N)
plt.plot(t_, v_, t_, v1_, t_, v2_, t_, v3_,t_, v4_,t_, v5_)
plt.xlabel("time (days)")
plt.ylabel(stype + " (cm)")
plt.legend(["total", "tap root", "long lateral", "short lateral", 'seminal roots', 'crown roots'])
plt.savefig("results/example_2d.png")
plt.show()
