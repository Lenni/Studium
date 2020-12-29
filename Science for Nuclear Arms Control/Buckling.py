import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from tqdm import tqdm

########### KONSTANTEN ############

rho = 19830  # kg/m^3
rho_comp = 7.3767 * rho # kg/m^3

n_T = 6.023 * 10 ** 23 / ((0.239) / (rho))  # 1/m^3
sig_F = 1.802 * 10 ** -28 * n_T  # m
sig_A = 1.855 * 10 ** -28 * n_T  # m
sig_S = 13.372 * 10 ** -28 * n_T  # m

nu = 3.172  # m/s

D = 1 / (3 * sig_S)

M_N = 1.6 * 10 ** -27  # kg

E_Fis = 175.8 + 5.9 + 5.3  # MeV


###################################

def R(r_0, B_G):
    return (B_G * r_0 - np.arctan(B_G * r_0) + np.pi) / (B_G)


def M(R, r_0, _rho = rho):
    return _rho * ((4 / 3 * np.pi * R ** 3) - (4 / 3 * np.pi * r_0 ** 3))


B_M = np.sqrt((nu * sig_F - sig_A) / (D))

r_0s = np.linspace(0, 0.1, 100)

Rs = R(r_0s, B_M)
Ms = M(Rs, r_0s)

plt.plot(r_0s, Rs)
plt.ylim(0, max(Rs) * 1.2)

plt.fill_between(r_0s, Rs, 10000, color="red", interpolate=True, alpha=0.2, label="(Super)Critical Region")

plt.xlabel("Inner Radius in m")
plt.ylabel("Outer Radius in m")
plt.legend()
plt.title("Critical Radius of a Hollow Pu-239 Sphere")

plt.show()

plt.plot(r_0s, Ms)
plt.ylim(0, max(Ms) * 1.2)

plt.fill_between(r_0s, Ms, 10000, color="red", interpolate=True, alpha=0.2, label="(Super)Critical Region")

###### SET POINT ######

m = 35
R_O = 0.086
r_i = np.cbrt(R_O ** 3 - (3 * m) / (4 * np.pi * rho))
plt.plot(r_i, m, label="Sample Device (Uncompressed)", marker="o")

#######################


plt.legend()
plt.xlabel("Inner Radius in m")
plt.ylabel("Mass in kg")

plt.title("Critical Mass of a Hollow Pu-239 Sphere")

plt.show()

############### Rerun Program with higher Density ##############


########### KONSTANTEN ############


n_T = 6.023 * 10 ** 23 / ((0.239) / (rho_comp))  # 1/m^3
sig_F = 1.802 * 10 ** -28 * n_T  # m
sig_A = 1.855 * 10 ** -28 * n_T  # m
sig_S = 13.372 * 10 ** -28 * n_T  # m


D = 1 / (3 * sig_S)
###################################


B_M = np.sqrt((nu * sig_F - sig_A) / (D))

r_0s = np.linspace(0, 0.1, 100)

Rs = R(r_0s, B_M)
Ms = M(Rs, r_0s, _rho = rho_comp)

plt.plot(r_0s, Rs)
plt.ylim(0, max(Rs) * 1.2)

plt.fill_between(r_0s, Rs, 10000, color="red", interpolate=True, alpha=0.2, label="(Super)Critical Region")

plt.xlabel("Inner Radius in m")
plt.ylabel("Outer Radius in m")
plt.legend()
plt.title("Critical Radius of a Hollow Pu-239 Sphere (Compressed)")

plt.show()

plt.plot(r_0s, Ms)
plt.ylim(0, max(Ms) * 1.2)

plt.fill_between(r_0s, Ms, 10000, color="red", interpolate=True, alpha=0.2, label="(Super)Critical Region")

###### SET POINT ######

M = 35
R_O = 0.086
r_i = np.cbrt(R_O ** 3 - (3 * M) / (4 * np.pi * rho))
plt.plot(0, M, label="Sample Device (Compressed)", marker="o")

#######################


plt.legend()
plt.xlabel("Inner Radius in m")
plt.ylabel("Mass in kg")

plt.title("Critical Mass of a Hollow Pu-239 Sphere (Compressed)")

plt.show()
