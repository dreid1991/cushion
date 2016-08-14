import sys
from math import *
from random import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', size=14)
sys.path.append('/home/daniel/Documents/cushion/build/python/build/lib.linux-x86_64-2.7/')
from Cush import *
def toGauge(p):
    return (p-101325)/101325.
def toAtm(p):
    return p/101325.
objectiveInit = 1000000000.
trialMoveSize = 0.00005
def permuteHoles(holes):
    idx = int(random() * len(holes))
    val = holes[idx]
    if random() > 0.5:
        val += trialMoveSize
    else:
        val -= trialMoveSize
    if val < 0:
        val = 0
    holes[idx] = val
    return holes

monteCarloTemp = 1.

def run(holes):
    #return Sim.run(velImp=25, massImp=1, vol=.01, holeSizes=holes) #ORIG
    return Sim.run(velImp=25, massImp=1, vol=.025, holeSizes=holes)
def evalObjective(holes, targetPressure):
    res = run(holes)
    if res.failed:
        return 100
    print toGauge(res.avgPressure), toAtm(res.stdevPressure)
    return abs(res.avgPressure - targetPressure) + res.stdevPressure

def plot(holes, iteration):
    res = run(holes)
    plt.plot(list(res.depths), [toGauge(x) for x in list(res.pressures)], '-', linewidth=2.5, label=str(iteration))
    #plt.plot(list(res.depths), list(res.molesTotal), '-', linewidth=2.5, label=str(iteration))
    #plt.plot(list(res.depths), list(res.velocities), '-', linewidth=2.5, label=str(iteration))

def iterate(targetPressure):
    #holes = list(np.linspace(0, 0.005, 50)) #ORIG
    holes = list(np.linspace(0, 0.005, 50)) #ORIG
    objective = evalObjective(holes, targetPressure)
    plot(holes, 0)
    for i in range(1):
        holesTrial = permuteHoles(holes[:])
        objectiveTrial = evalObjective(holesTrial, targetPressure)
        if objectiveTrial < objective:
            holes = holesTrial
            objective = objectiveTrial
        else:
            dFit = objectiveTrial - objective
            prob = exp(-dFit / monteCarloTemp)
            if random() < prob:
                holes = holesTrial
                objective = objectiveTrial
        print holes
    print holes
    return holes


#holes = iterate(0.6)
holes = list(np.linspace(0, 0.005, 50)) #ORIG
plot(holes, 1)
plt.xlabel('Impactor depth (meters)')
plt.ylabel('Pressure (atm)')
plt.legend()
plt.show()


#res = Sim.run(velImp=5, massImp=1, vol=.01, holeSizes=[0.0005])
#res2 = Sim.run(velImp=25, massImp=1, vol=.01, holeSizes=[0.00])
#plt.plot(list(res.times), [toGauge(x) for x in list(res.pressures)])
#plt.plot(list(res2.depths), [toGauge(x) for x in list(res2.pressures)], '-', linewidth=2.5)
#plt.xlabel('Impactor depth (meters)')
#plt.ylabel('Pressure (atm)')
#plt.savefig('ideal_gas_compare.svg')
#plt.show()
#plt.clf()
#plt.plot(list(res2.times), list(res2.velocities))
#plt.show()
