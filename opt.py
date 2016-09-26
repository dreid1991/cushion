import sys
import os
import copy
from math import *
from random import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', size=22)
sys.path.append('/home/daniel/Documents/cushion/build/python/build/lib.linux-x86_64-2.7/')
from Cush import *

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
trialMoveSize = 0.00001
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
    return Sim.run(velImp=runInfo.velocityImp, massImp=runInfo.massImp, vol=runInfo.volSys, holeSizes=runInfo.holes, dt=1e-7, writeEvery=1)

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

    plot(runInfo, 'Loaded')
    objective = evalObjective(runInfo)
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
           # print 'prob %f arg %f ' % (prob, dFit)
            if random() < prob:
                runInfo.holes = holesTrial
                objective = objectiveTrial
        if objective < 0.03:
            break
        print i, objective
        #print holes
    return runInfo


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

#writeInfo('setup.dat', RunInfo(25, 1, 0.025, np.linspace(0, 0.005, 50)))
#appromiximating ball as 8cm * 8cm * 8cm cube
surfAreaActual = 0.08 * 0.08 #m^2
nBalls = 4
vol = 1.0 * 1.0 * 0.08 * nBalls
holesInit = [0.] * nBalls
massReal = 0.5 #kg
massImp = massReal / surfAreaActual
x = 5 #meters
a = 9.81 #m/s^2
vImpact = 10#sqrt(2*x*a)

plot(RunInfo(vImpact, massImp, vol, holesInit), 'Initial')
#if os.path.isfile('out.dat'):
info = readInfo('out_opt.dat')
#else:
#    info = RunInfo(vImpact, massImp, vol, holesInit)
#writeInfo('setup.dat', RunInfo(vImpact, massImp, vol, holesInit))
#runInfo = iterate(10000, runInfo = info)
#os.system('mv out.dat out_prev.dat')
#writeInfo('out.dat', runInfo)
res = plot(info, 'Final')
plt.xlabel('Impactor depth (cm)')
plt.ylabel('Pressure (atm)')
plt.ylim(0., 0.8)
plt.tight_layout()
#plt.savefig('opt.png')
plt.clf()
colors = ['r', 'g', 'b', 'k']
for i in range(nBalls):
    moles = [x[i] for x in res.molesPer]
    dMolesDt = [(res.molesPer[j+1][i] - res.molesPer[j][i]) / (res.times[j+1] - res.times[j]) for j in range(0, len(res.times)-1)]
    dMolesDtCalc = [calcDMoles(pressure, info.holes[i]) for pressure in res.pressures]
    plt.plot(res.times, dMolesDtCalc, '--', color=colors[i], linewidth=3.5)
    #plt.plot(res.times, moles, linewidth=2.5)
    plt.plot(list(res.times)[:-1], dMolesDt, linewidth=2.5, color=colors[i])
press = [toGauge(p) for p in res.pressures]
plt.plot(res.times, press)

plt.xlabel('Times')
plt.ylabel('n moles')


plt.tight_layout()
#plt.savefig('nmoles.svg')
#plt.savefig('nmoles.png')
plt.show()
'''
opt = readInfo('out_opt.dat')
maxZ = 11
for i, x in enumerate(np.linspace(0, 320, maxZ)[1:]):
    print x* 0.08**2
    opt.massImp= x
    #opt.velocityImp= x
    plot(opt, 'V = %04f' % x, zorder = maxZ-i)
plt.xlabel('Depth (cm)')
plt.ylabel('Pressure (atm)')
#plt.xlim(0, 32)
plt.ylim(0, 4)
plt.tight_layout()
for x in ['png', 'svg']:
    plt.savefig('impact_to_320_kg.%s' % x)
plt.show()
'''





exit()

