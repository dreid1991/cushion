import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', size=22)
sys.path.append('/home/daniel/Documents/cushion/build/python/build/lib.linux-x86_64-2.7/')
from Cush import *
def toGauge(p):
    return (p-101325)/101325.
#res = Sim.run(velImp=5, massImp=1, vol=.01, holeSizes=[0.0005])
res2 = Sim.run(velImp=25, massImp=1, vol=.025, holeSizes=[0.00])
#plt.plot(list(res.times), [toGauge(x) for x in list(res.pressures)])
vols = [0.025 - x for x in list(res2.depths)]
molesTotal = list(res2.molesTotal)
pressures = [r[0]*8.31*300/r[1] for r in zip(molesTotal, vols)]

plt.plot([100*x for x in list(res2.times)], [toGauge(x) for x in list(res2.pressures)], '-', linewidth=2.5, label='Model', color='blue')
plt.plot([100*x for x in list(res2.times)], [toGauge(x) for x in pressures], '--', linewidth=2.5, color='red', label='Ideal gas')


res2 = Sim.run(velImp=25, massImp=1, vol=.025, holeSizes=[0.05])
#plt.plot(list(res.times), [toGauge(x) for x in list(res.pressures)])
vols = [0.025 - x for x in list(res2.depths)]
molesTotal = list(res2.molesTotal)
pressures = [r[0]*8.31*300/r[1] for r in zip(molesTotal, vols)]

plt.plot([100*x for x in list(res2.times)], [toGauge(x) for x in list(res2.pressures)], '-', linewidth=2.5, color='blue')
plt.plot([100*x for x in list(res2.times)], [toGauge(x) for x in pressures], '--', linewidth=2.5, color='red')
#plt.plot([100*x for x in list(res2.times)], list(res2.molesTotal), linewidth=2.5)


#plt.xlabel('Impactor depth (cm)')
plt.xlabel('Time (sec)')
#plt.ylabel('Pressure (atm)')
plt.ylabel('Moles')
plt.legend(loc='upper left')
#plt.xlim(0, 2.5)
#plt.ylim(0, 1.1)
plt.tight_layout()
plt.savefig('ideal_gas_compare.svg')
plt.show()
#plt.clf()
#plt.plot(list(res2.times), list(res2.velocities))
#plt.show()
