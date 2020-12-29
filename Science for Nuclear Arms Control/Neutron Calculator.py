import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


########### KONSTANTEN ############

sig_F = 1.802 * 10**-28 # m^2
k_eff = 1.05423

E_N = 1*10**6 * 1.6 * 10**-19 #J
M_N = 1.6*10**-27 #kg
N_0 = 19830*6.023*10**23/(0.239) # 1/m^3

E_Fis = 175.8 + 5.9 + 5.3 #MeV

###################################

v = np.sqrt(2*E_N/M_N)
i = 0
t = 0

N = N_0
N_Fis = 0

ts = []
ls = []
Ns = []
N_Fiss = []
dNs = []

while(N/N_0 > 0.1):

    l = 1 / ( N * sig_F * v)
    dt = l

    dN = N * dt*sig_F*v*k_eff**(t /dt)
    N = N - dN
    N_Fis = N_Fis + dN

    N_Fiss.append(N_Fis)
    Ns.append(N)
    dNs.append(dN)
    ts.append(t)
    ls.append(l)

    t = t + dt
    i = i+1

plt.plot(ts, dNs, label="Fission Rate")
plt.title("Fission Rate of supercritical Pu-239")
plt.legend()
plt.xlabel("t in s")
plt.ylabel("N Fissions")

plt.show()

plt.plot(ts, Ns, label="Pu-239 Nuclei")
plt.title("Fissile Material Density")
plt.legend()
plt.xlabel("t in s")
plt.ylabel("N Fissile Nuclei")

plt.show()

plt.plot(ts, ls, label="Mean Lifetime")
plt.title("Neutron Lifetime")
plt.legend()
plt.xlabel("t in s")
plt.ylabel("Lifetime in s")

plt.show()

plt.plot(ts, np.array(N_Fiss) * E_Fis, label="Energy")
plt.title("Energy Released by a Nuclear Device")
plt.legend()
plt.xlabel("t in s")
plt.ylabel("E in MeV")

plt.show()
print("It took {} Generations to Fission the Device".format(i))
print("Fission Time: {} s".format(t))