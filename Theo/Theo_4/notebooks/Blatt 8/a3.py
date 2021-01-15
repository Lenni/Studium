#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import division,print_function,absolute_import,unicode_literals

import math
import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt
from tqdm import tqdm

import spinop

steps = 500
min = 0.001
max = 5

def innereEnergie(E_gs, energies_norm, T):

    sum1 = 0
    sum2 = 0
    for i in range(0, len(energies_norm)):
        en = energies_norm[i]
        exp = -en / T
        sum1 += math.exp(exp)

        sum2 += en * np.exp(exp)

    return E_gs + 1 / sum1 * sum2

def entropie(energies_norm, T):
    sum1 = 0
    sum2 = 0
    for i in range(0, len(energies_norm)):
        en = energies_norm[i]
        exp = -en / T
        sum1 += math.exp(exp)

        sum2 += np.exp(exp) * en / T**2

    return np.log(sum1) + T * sum2 / sum1

def cv(energies_norm, T):
    s1 = 0
    s2 = 0
    s3 = 0
    s4 = 0

    for i in range(0, len(energies_norm)):
        en = energies_norm[i]
        exp = -en / T

        s1 += en * np.exp(exp) * en / (T**2)
        s2 += np.exp(exp)
        s3 += en * np.exp(exp)
        s4 += en / (T**2) * np.exp(exp)

    return (s1 * s2 - s3 * s4) / (s2**2)


def calc(Ns):
    # Build the Hamiltonian

    # Formel: H = S_1*S_2 = S^x_1*S^x_1 + S^y_1*S^y_2 + S^z_1*S^z_2
    H = sparse.csr_matrix((2**Ns,2**Ns),dtype=np.complex128)

    for i in range(1, Ns):
        H += spinop.Sx(i, N=Ns).dot(spinop.Sx(i+1, N=Ns))
        H += spinop.Sy(i, N=Ns).dot(spinop.Sy(i+1, N=Ns))
        H += spinop.Sz(i, N=Ns).dot(spinop.Sz(i+1, N=Ns))


    # Diagonalization
    H_full = H.toarray()
    energies,evecs = np.linalg.eigh(H_full)

    energy_gs = energies[0]
    energies_norm = energies-energy_gs
    print("Ground state energy:", energy_gs)
    print("Energies:")

    T = np.linspace(min,max,steps)
    E = np.zeros(steps)
    S = np.zeros(steps)
    Cv = np.zeros(steps)

    for i in tqdm(range(0, steps)):
        E[i] = innereEnergie(energy_gs, energies_norm, T[i])
        S[i] = entropie(energies_norm, T[i])
        Cv[i] = cv(energies_norm, T[i])

    return energy_gs, energies, energies_norm, E, S, Cv

def plotCompare(title, data9, data10):
    T = np.linspace(min, max, steps)
    fig, axs = plt.subplots(1, figsize=(16,9))
    axs.set_title(title)
    plt.xlabel("Temperatur T")
    axs.plot(T, data9, label="9")
    axs.plot(T, data10, label="10")
    plt.legend()
    plt.savefig(title + ".png")
    plt.show()



energy_gs1, energies1, energies_norm1, E1, S1, Cv1 = calc(1)
energy_gs2, energies2, energies_norm2, E2, S2, Cv2 = calc(2)
energy_gs3, energies3, energies_norm3, E3, S3, Cv3 = calc(3)
energy_gs4, energies4, energies_norm4, E4, S4, Cv4 = calc(4)
energy_gs5, energies5, energies_norm5, E5, S5, Cv5 = calc(5)
energy_gs6, energies6, energies_norm6, E6, S6, Cv6 = calc(6)
energy_gs7, energies7, energies_norm7, E7, S7, Cv7 = calc(7)
energy_gs9, energies9, energies_norm9, E9, S9, Cv9 = calc(9)
energy_gs10, energies10, energies_norm10, E10, S10, Cv10 = calc(10)

plotCompare('Innere Energie', E9, E10)
plotCompare('Entropie', S9, S10)
plotCompare('Waermekapazitaet', Cv9, Cv10)

T = np.linspace(min, max, steps)
fig, axs = plt.subplots(1)
axs.set_title("Energievergleich")
plt.xlabel("Temperatur T")
axs.plot(T, E1, label="1")
axs.plot(T, E2, label="2")
axs.plot(T, E3, label="3")
axs.plot(T, E4, label="4")
axs.plot(T, E5, label="5")
axs.plot(T, E6, label="6")
axs.plot(T, E7, label="7")
axs.plot(T, E9, label="9")
axs.plot(T, E10, label="10")
plt.legend()
plt.show()
