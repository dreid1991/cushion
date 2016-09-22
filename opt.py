import sys
from math import *
from random import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', size=22)
sys.path.append('/home/daniel/Documents/cushion/build/python/build/lib.linux-x86_64-2.7/')
from Cush import *
import copy

class RunInfo:
    def __init__(self, velocityImp, massImp, volSys, holes):
        self.velocityImp = velocityImp
        self.massImp = massImp
        self.volSys = volSys
        self.holes = holes

def toGauge(p):
    return (p-101325)/101325.
def toAtm(p):
    return p/101325.
objectiveInit = 1000000000.
trialMoveSize = 0.000001
def permuteHoles(holes):
    idx = int(random() * (len(holes)-1))+1 #so ignoring first hole - stays at zero
    val = holes[idx]
    if random() > 0.5:
        val += trialMoveSize
    else:
        val -= trialMoveSize
    if val < 0:
        val = 0
    holes[idx] = val
    return holes

monteCarloTemp = .000002

def run(runInfo):
   # return Sim.run(velImp=25, massImp=1, vol=.01, holeSizes=holes) #ORIG
    return Sim.run(velImp=runInfo.velocityImp, massImp=runInfo.massImp, vol=runInfo.volSys, holeSizes=runInfo.holes, dt=1e-7, writeEvery=10)

def evalObjective(runInfo):
    res = run(runInfo)
    if res.failed:
        return 100
    print toGauge(res.avgPressure), toAtm(res.stdevPressure)
    return toGauge(res.avgPressure) + toAtm(res.stdevPressure)

def plot(runInfo, iteration):
    res = run(runInfo)
    print len(res.depths)
    print len(res.pressures)
    plt.plot([100*x for x in list(res.depths)], [toGauge(x) for x in list(res.pressures)], '-', linewidth=2.5, label=iteration)
    #plt.plot(list(res.times), list(res.velocities), '-', linewidth=2.5, label=iteration)



def readInfo(src):
    f = open(src, 'r')
    lines = f.readlines()
    velocity = float(lines[0].split()[1])
    mass = float(lines[1].split()[1])
    volSys = float(lines[2].split()[1])
    holes = eval(lines[3])
    return RunInfo(velocity, mass, volSys, holes)


def writeInfo(fn, runInfo):
    f = open(fn, 'w')
    f.write('velocityImp %f\n' % runInfo.velocityImp)
    f.write('massImp %f\n' % runInfo.massImp)
    f.write('volSys %f\n' % runInfo.volSys)
    f.write(repr(list(runInfo.holes)))
    f.close()
#return Sim.run(velImp=25, massImp=1, vol=.025, holeSizes=holes)


def iterate(nTurns, src=None, runInfo=None):
    #holes = list(np.linspace(0, 0.005, 50)) #ORIG
    if runInfo == None:
        runInfo = readInfo(src)

    plot(runInfo, 'Initial')
    return runInfo
    objective = evalObjective(runInfo)
    for i in range(nTurns):
        print 'hi'
        holesTrial = permuteHoles(runInfo.holes[:])
        infoTrial = copy.deepcopy(runInfo)
        infoTrial.holes = holesTrial
        objectiveTrial = evalObjective(infoTrial)
        if objectiveTrial < objective:
            runInfo.holes = holesTrial
            objective = objectiveTrial
        else:
            dFit = objectiveTrial - objective
            prob = exp(-dFit / monteCarloTemp)
           # print 'prob %f arg %f ' % (prob, dFit)
            if random() < prob:
                runInfo.holes = holesTrial
                objective = objectiveTrial
        print objective
        if objective < 0.03:
            break
        #print holes
    print holes
    return runInfo

#writeInfo('setup.dat', RunInfo(25, 1, 0.25, np.linspace(0, 0.005, 50)))
writeInfo('setup.dat', RunInfo(25, 1, 0.025, np.linspace(0, 0.005, 50)))
res = iterate(30, 'setup.dat')
writeInfo('out.dat', res)
plt.show()
        #plot(list(np.linspace(0, 0.005, 50)), 'Unoptimized')

#holes = iterate() #target not used
#plt.xlabel('Impactor depth (cm)')
#plt.ylabel('Pressure (atm)')
#plt.legend(loc='upper left')

#plt.ylim(0, 1.1)
#plt.tight_layout()
##plt.show()
#plt.show()
#plt.savefig('opt.png')

exit()
#f = open('holes.dat', 'w')
#f.write(str(holes))
#f.close()
#holes = list(np.linspace(0, 0.005, 50)) #ORIG
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



