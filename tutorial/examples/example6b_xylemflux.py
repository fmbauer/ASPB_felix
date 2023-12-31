""" water movement within the root (static soil) """
import sys; sys.path.append("../.."); sys.path.append("../../src/")

import plantbox as pb
import visualisation.vtk_plot as vp
from functional.xylem_flux import XylemFluxPython

import numpy as np
import matplotlib.pyplot as plt

""" Parameters """
kz = 4.32e-2  # axial conductivity [cm^3/day]
kr = 1.728e-4  # radial conductivity [1/day]
p_s = -200  # static soil pressure [cm]
p0 = -500  # dircichlet bc at top
simtime = 60  # [day] for task b
dt = 1.

""" root system """
rs = pb.MappedRootSystem()
path = "../../modelparameter/structural/plant/"
name = "P3_rs"  # Zea_mays_1_Leitner_2010
rs.readParameters(path + name + ".xml")
rs.initialize()
rs.simulate(simtime, False)

""" root problem """
r = XylemFluxPython(rs)
r.setKr([kr * 0, kr, kr , kr, kr, kr])
r.setKx([kz, kz, kz, kz, kz, kz])
nodes = r.get_nodes()
soil_index = lambda x, y, z: 0
r.rs.setSoilGrid(soil_index)
suf=r.get_suf(simtime)
""" Numerical solution """
rx = r.solve_dirichlet(simtime, p0, p_s, [p_s], True)
# trans = -1.185
# rx = r.solve_neumann(simtime, trans, [p_s], True)
fluxes = r.segFluxes(simtime, rx, -200 * np.ones(rx.shape), False)  # cm3/day
print("Transpiration", r.collar_flux(simtime, rx, [p_s]), "cm3/day")

""" plot results """
plt.plot(suf, nodes[1:, 2],'o',color='darkred',markersize=1)
plt.xlabel("SUF")
plt.ylabel("Depth (m)")
plt.title("Standard uptake fraction")
plt.show()

""" Additional vtk plot """
print("rx", rx.shape)
print("fluxes", len(fluxes))
print("segments", len(rs.getSegments()))
ana = pb.SegmentAnalyser(r.rs.mappedSegments())
print(len(ana.nodes))
print(len(ana.segments))
ana.addData("rx", rx)
ana.addData("suf", suf)

ana.addData("fluxes", np.maximum(fluxes, -1.e-3))  # cut off for vizualisation
# vp.plot_roots(ana, "suf", "Xylem matric potential (cm)")  # "fluxes", subType
# vp.plot_roots(ana, "rx", "Xylem matric potential (cm)")  # "fluxes", subType
ana.write("results/P3_roots.vtp")





# print("\tsum of SUF",np.around( np.sum(suf),2), "summed positive",np.around( np.sum(suf[suf >= 0]),2) )
