import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', size=14)
sys.path.append('/home/daniel/Documents/cushion/build/python/build/lib.linux-x86_64-2.7/')
from Cush import *
def toGauge(p):
    return (p-101325)/101325.
#res = Sim.run(velImp=5, massImp=1, vol=.01, holeSizes=[0.0005])
res2 = Sim.run(velImp=50, massImp=1, vol=.01, holeSizes=[0.01])
#plt.plot(list(res.times), [toGauge(x) for x in list(res.pressures)])
vols = np.linspace(0.001, 0.01, 100)
n = 0.406242
pressures = [toGauge(n*8.314*300/v) for v in vols]
depths = [0.01-v for v in vols]
plt.plot(list(res2.depths), [toGauge(x) for x in list(res2.pressures)], '-', linewidth=2.5)
plt.plot(depths, pressures, '--', linewidth=2.5, color='red')
plt.xlabel('Impactor depth (meters)')
plt.ylabel('Pressure (atm)')
#plt.savefig('ideal_gas_compare.svg')
plt.show()
#plt.clf()
#plt.plot(list(res2.times), list(res2.velocities))
#plt.show()
