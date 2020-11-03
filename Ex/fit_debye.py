from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt


def func(x, D_T):
    return 12/5 * np.pi**4 * 8.314 * (x/D_T)**3


T = [0.1, 1, 5, 8, 10, 15, 20]
C = [8.5*10**(-7), 8.6*10**(-4), 0.12, 0.59, 1.1, 2.8, 6.3]

popt, pcov = curve_fit(func, T, C)
print(popt)


plt.plot(T, C)
plt.plot(T, func(np.array(T), popt[0]))

plt.show()
