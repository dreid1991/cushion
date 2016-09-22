import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', size=22)
f = open('holes.dat', 'r')
holes = sorted(eval(f.readline()))
plt.plot(holes, linewidth=3)
plt.plot([0, 49], [0, 0.005], linewidth=3)
plt.ylabel('Hole size ($m^{2}$)')
plt.xlabel('Section number')
plt.tight_layout()
plt.savefig('opt_sizes.png')
