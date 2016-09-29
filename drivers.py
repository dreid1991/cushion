import sys
import os
import copy
from math import *
from random import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', size=22)
sys.path.append('/home/daniel/Documents/cushion/core/build/python/build/lib.linux-x86_64-2.7/')
from Cush import *

objectiveInit = 1000000000.
trialMoveSize = 0.00001
monteCarloTemp = .000002

class RunInfo:
    def __init__(self, velocityImp, massImp, volSys, holes):
        self.velocityImp = velocityImp
        self.massImp = massImp
        self.volSys = volSys
        self.holes = holes
        self.objective = objectiveInit

def toGauge(p):
    return (p-101325)/101325.
def toAtm(p):
    return p/101325.
def permuteHoles(holes):
    idx = int(random() * (len(holes)-1))+1 #so ignoring first hole - stays at zero
    if idx < len(holes):
        val = holes[idx]
        if random() > 0.5:
            val += trialMoveSize
        else:
            val -= trialMoveSize
        if val < 0:
            val = 0
        holes[idx] = val
    return holes


def run(runInfo):
   # return Sim.run(velImp=25, massImp=1, vol=.01, holeSizes=holes) #ORIG
    return Sim.run(velImp=runInfo.velocityImp, massImp=runInfo.massImp, vol=runInfo.volSys, holeSizes=runInfo.holes, dt=1e-7, writeEvery=10)

def evalObjective(runInfo):
    res = run(runInfo)
    if res.failed:
        return 1e10
    return Analyze.integralSqr(res.depths, Analyze.add(res.pressures, -101325))
def plot(runInfo, iteration, zorder = 1):
    res = run(runInfo)
    plt.plot([100*x for x in list(res.depths)], [toGauge(x) for x in list(res.pressures)], '-', linewidth=2.5, label=iteration, zorder=zorder)
    #plt.plot(list(res.times), list(res.velocities), '-', linewidth=2.5, label=iteration)
    return res

def readInfo(src):
    f = open(src, 'r')
    lines = f.readlines()
    velocity = float(lines[0].split()[1])
    mass = float(lines[1].split()[1])
    volSys = float(lines[2].split()[1])
    monteCarloTemp = float(lines[3].split()[1])
    trialMoveSize = float(lines[4].split()[1])
    holes = eval(lines[5])
    return RunInfo(velocity, mass, volSys, holes)


def writeInfo(fn, runInfo):
    f = open(fn, 'w')
    f.write('velocityImp %f\n' % runInfo.velocityImp)
    f.write('massImp %f\n' % runInfo.massImp)
    f.write('volSys %f\n' % runInfo.volSys)
    f.write('monteCarloTemp %f\n' % monteCarloTemp)
    f.write('trialMoveSize %f\n' % trialMoveSize)
    f.write(repr(list(runInfo.holes)))
    f.close()


def iterate(nTurns, src=None, runInfo=None):

    if runInfo == None:
        runInfo = readInfo(src)
    else:
        runInfo = copy.deepcopy(runInfo)

    objective = evalObjective(runInfo)
    objectives = []
    for i in range(nTurns):
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
            if random() < prob:
                runInfo.holes = holesTrial
                objective = objectiveTrial
        if objective < 0.03:
            break
        print i, objective
    runInfo.objective = objective
    return runInfo

'''
#for validation
def calcDMoles(pressure, holeSize):

    pressureG = toGauge(pressure) * 101325
    molesPerVolume = pressure / (8.314 * 300)
    massPerMole = 0.028*0.79 + 0.032 * 0.21
    massPerVol = molesPerVolume * massPerMole
    #massSpc = 1.275#from wiki, calc to verify
    v = sqrt(2*pressureG / massPerVol)
    print 'velPy %f' % v
    volumeLeaving = v * holeSize
    nMolesLeaving = molesPerVolume * volumeLeaving
    return -nMolesLeaving
'''
if __name__ == '__main__':
    info = readInfo('../procd/out.dat')
    plot(info, 'test')
    plt.show()

